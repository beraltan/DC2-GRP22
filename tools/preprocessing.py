import os
import pandas as pd
from glob import glob


def lsoa_to_borough_mapping():
    """
    This function reads a CSV file containing LSOA data and performs preprocessing steps to create a mapping between LSOA codes and borough names.
    
    Returns:
    None
    """
    
    # Read the LSOA data from the CSV file
    data = pd.read_csv('data/secondary_data/lsoa_data/lsoa_data_iadatasheet1.csv')
    
    # Remove unnecessary rows from the data
    data = data.iloc[3:]
    
    if 'Unnamed: 0' in data.columns:
        # Create the 'borough' column by stripping the numeric suffix and any whitespace from the 'Unnamed: 0' column
        data['Borough'] = data['Unnamed: 1'].str.extract(r'(^[\D\s]+)').apply(lambda x: x.str.strip())
        
        # Get the position of the 'Unnamed: 0' column
        idx = data.columns.get_loc('Unnamed: 0')
        
        # Rearrange columns to place 'borough' right after 'Unnamed: 0'
        cols = list(data.columns)
        # Move 'borough' to the right position
        new_cols = cols[:idx+1] + ['Borough'] + cols[idx+1:-1]  # assuming 'borough' is the last in the list
        data = data[new_cols]
        
        # Save the modified dataframe back to CSV or return it
        
        
    # Create the 'lookup_tables' directory if it does not exist
    lookup_tables_dir = 'data/lookup_tables'
    if not os.path.exists(lookup_tables_dir):
        os.makedirs(lookup_tables_dir)
    
    # Rename 'Unnamed: 0' column to 'LSOA code'
    data.rename(columns={'Unnamed: 1': 'LSOA_name'}, inplace=True)
    data.rename(columns={'Unnamed: 0': 'LSOA_code'}, inplace=True)
    data = data[['LSOA_name', 'LSOA_code', 'Borough']]
    
    data.to_csv('data/lookup_tables/lsoa2borough.csv', index=False)
    # Display the first few rows of the data


lsoa_to_borough_mapping()



def add_borough_column(base_dir, file_patterns, lookup_table_path):
    # Load the lookup table from the provided CSV file
    borough_lookup = pd.read_csv(lookup_table_path, low_memory=False)

    # Define potential LSOA column names to check for in the files
    lsoa_col_variants = ['LSOA code', 'LSOA_code']

    # Walk through the directory structure
    for root, _, files in os.walk(base_dir):
        for file in files:
            # Check if the file matches any of the patterns
            for pattern in file_patterns:
                if pattern in file:
                    # Read the CSV file
                    file_path = os.path.join(root, file)
                    data = pd.read_csv(file_path)

                    # Find the correct LSOA column name
                    lsoa_col = next((col for col in lsoa_col_variants if col in data.columns), None)

                    # If a matching LSOA column name is found
                    if lsoa_col:
                        # Merge the 'Borough' data using the found LSOA column name
                        data_with_borough = pd.merge(data, borough_lookup, left_on=lsoa_col, right_on='LSOA_code', how='left')

                        # Ensure the 'Borough' column is right next to the LSOA column
                        
                        lsoa_index = data_with_borough.columns.tolist().index(lsoa_col)
                        # Reorder columns to place 'Borough' next to the LSOA code
                        columns = data_with_borough.columns.tolist()
                        
                        data_with_borough = data_with_borough[columns]

                        # Save the updated DataFrame back to the file
                        data_with_borough.to_csv(file_path, index=False)
                        print(f'Updated file: {file_path}')
                        
# Base directory path
base_dir = './data/primary_data'
lookup_table_path = './data/lookup_tables/lsoa2borough.csv'

# List of unique patterns to match files for updating
file_patterns = [
    'metropolitan-stop-and-search', 'city-of-london-street', 'btp-street', 
    'metropolitan-street', 'city-of-london-stop-and-search', 'metropolitan-outcomes', 
    'city-of-london-outcomes', 'btp-stop-and-search'
]

# Call the function with the base directory, list of file patterns, and path to the lookup table
add_borough_column(base_dir, file_patterns, lookup_table_path)


def concatenate_csv_files(base_dir, file_patterns):
    # Create a new directory for concatenated CSVs
    concatenated_dir = os.path.join(base_dir, 'concatenated_csvs')
    os.makedirs(concatenated_dir, exist_ok=True)
    
    # Dictionary to hold the dataframes for each pattern
    dataframes_dict = {pattern: [] for pattern in file_patterns}
    
    # Walk through the directory structure
    for root, _, files in os.walk(base_dir):
        for file in files:
            # Check if the file matches any of the patterns
            for pattern in file_patterns:
                if pattern in file:
                    # Read the CSV file and append to the correct list
                    df = pd.read_csv(os.path.join(root, file))
                    dataframes_dict[pattern].append(df)
                    break
    
    # Now concatenate the dataframes for each pattern and write to a CSV file
    for pattern, dfs in dataframes_dict.items():
        if dfs:  # Check if there are any dataframes to concatenate
            concatenated_df = pd.concat(dfs, ignore_index=True)
            output_file = os.path.join(concatenated_dir, f'{pattern}.csv')
            concatenated_df.to_csv(output_file, index=False)
            print(f'Created file: {output_file} with {len(concatenated_df)} rows.')

# Base directory path
base_dir = './data/primary_data'

# List of unique patterns to match files for concatenation
file_patterns = [
    'metropolitan-stop-and-search', 'city-of-london-street', 'btp-street', 
    'metropolitan-street', 'city-of-london-stop-and-search', 'metropolitan-outcomes', 
    'city-of-london-outcomes', 'btp-stop-and-search'
]

# Call the function with the base directory and the list of file patterns
concatenate_csv_files(base_dir, file_patterns)