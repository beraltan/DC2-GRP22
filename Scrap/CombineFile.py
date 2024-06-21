import pandas as pd

# Load the data from the provided Excel files
file_path1 = "USE2-April23-Mar24.xlsx"
file_path2 = "../qwe/USE3-April22-Mar23.xlsx"

# Load both sheets from the first file
use_of_force_cases_1 = pd.read_excel(file_path1, sheet_name='UoF')
use_of_force_details_1 = pd.read_excel(file_path1, sheet_name='UoFPO')

# Load both sheets from the second file
use_of_force_cases_2 = pd.read_excel(file_path2, sheet_name='UoF')
use_of_force_details_2 = pd.read_excel(file_path2, sheet_name='UoFPO')

# Combine the two datasets
combined_cases = pd.concat([use_of_force_cases_1, use_of_force_cases_2], ignore_index=True)
combined_details = pd.concat([use_of_force_details_1, use_of_force_details_2], ignore_index=True)

# Save the combined dataset to a new Excel file
output_path =  r"C:\Users\danie\PycharmProjects\pythonProject4\Post_22.xlsx"
with pd.ExcelWriter(output_path) as writer:
    combined_cases.to_excel(writer, sheet_name='UoF', index=False)
    combined_details.to_excel(writer, sheet_name='UoFPO', index=False)

print(f"Combined dataset saved to {output_path}")
