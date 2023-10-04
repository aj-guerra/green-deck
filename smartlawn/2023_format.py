import pandas as pd

def extract_data_from_sheet(df, key_loc_h, key_loc_v, val_loc_h, val_loc_v):
    # Identify locations of the term "Average"
    locations = df[df == 'Average'].stack().index
    col_indices = df.columns
    col_index_mapping = {col: idx for idx, col in enumerate(col_indices)}
    locations = [(loc[0], col_index_mapping[loc[1]]) for loc in locations]

    # Extract the keys and values to create the dictionary
    average_dict = {}
    for location in locations:
        key = df.iloc[location[0]+key_loc_h, location[1]-key_loc_v]
        value = df.iloc[location[0]+val_loc_v, location[1]+val_loc_h]
        average_dict[key] = value

    return average_dict

def convert_to_dataframe(data):
    # Convert datetime.datetime to pandas.Timestamp
    converted_data = {pd.Timestamp(k): v for k, v in data.items() if k is not None}

    # Create DataFrame
    df = pd.DataFrame(list(converted_data.items()), columns=['Date', 'Value'])
    
    # Replace the '#DIV/0!' string with NaN for better handling in pandas
    df.replace('#DIV/0!', pd.NA, inplace=True)
    
    return df

def main():
    # Get file name (or path) input from user
    file_name = input("Please enter the name (or path) of the Excel file: ")
    key_loc_h = int(input("Where is the date located HORIZONTALLY relative to the 'Average' cell? Enter an integer, where negative is left and positive is right: "))
    key_loc_v = int(input("Where is the date located VERTICALLY relative to the 'Average' cell? Enter an integer, where negative is down and positive is up: "))
    val_loc_h = int(input("Where is the NDVI located HORIZONTALLY relative to the 'Average' cell? Enter an integer, where negative is left and positive is right: "))
    val_loc_v = int(input("Where is the NDVI located VERTICALLY relative to the 'Average' cell? Enter an integer, where negative is down and positive is up: "))
    # Load the excel file
    xls = pd.ExcelFile(file_name)

    # Process each sheet and store results in a dictionary with sheet names as keys
    result = {}
    for sheet_name in xls.sheet_names:
        df = pd.read_excel(xls, sheet_name=sheet_name)
        extracted_data = extract_data_from_sheet(df, key_loc_h, key_loc_v, val_loc_h, val_loc_v)
        result[sheet_name] = convert_to_dataframe(extracted_data)

    # Return results
    return result

if __name__ == '__main__':
    result_data = main()
    for sheet, df in result_data.items():
        print(f"\nSheet: {sheet}")
        print(df)
