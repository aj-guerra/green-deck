import pandas as pd
import os

def clean_sheet(df):
    # Remove rows with "NDVI"
    df = df[~df.applymap(lambda x: isinstance(x, str) and "ndvi" in x.lower()).any(axis=1)]
    # Remove rows with "average"
    df = df[~df.applymap(lambda x: isinstance(x, str) and "average" in x.lower()).any(axis=1)]
    # Remove rows where the first cell is empty
    df = df[df.iloc[:, 0].notna()]
    return df

def main():
    file_path = input("Please enter the path to the Excel file: ")
    
    # Create the output directory if it doesn't exist
    output_directory = "clean_files"
    if not os.path.exists(output_directory):
        os.makedirs(output_directory)
    
    # Prepare the output file path
    output_path = os.path.join(output_directory, os.path.basename(file_path))
    
    # Load the Excel file and get sheet names
    xls = pd.ExcelFile(file_path)
    sheet_names = xls.sheet_names
    
    with pd.ExcelWriter(output_path) as writer:
        for sheet in sheet_names:
            df = pd.read_excel(xls, sheet)
            cleaned_df = clean_sheet(df)
            cleaned_df.to_excel(writer, sheet_name=sheet, index=False)

    print(f"Cleaned file saved to: {output_path}")

if __name__ == "__main__":
    main()
