import pandas as pd

# Load the Excel file
file_path = r"C:\Users\danie\OneDrive\Data Challenege 2\regionalgrossdomesticproductgdplocalauthorities (1).xlsx"
xls = pd.ExcelFile(file_path)

# List the sheets in the Excel file
print(xls.sheet_names)

# Load each relevant sheet into a DataFrame
gdp_per_head = pd.read_excel(xls, sheet_name='Table 7')
population = pd.read_excel(xls, sheet_name='Table 6')
gdp_growth_rate = pd.read_excel(xls, sheet_name='Table 12')
vat = pd.read_excel(xls, sheet_name='Table 2')

# Save the extracted data to CSV files
gdp_per_head.to_csv('C:\\Users\\danie\\PycharmProjects\\pythonProject4\\gdp_per_head.csv', index=False)
population.to_csv('C:\\Users\\danie\\PycharmProjects\\pythonProject4\\population.csv', index=False)
gdp_growth_rate.to_csv('C:\\Users\\danie\\PycharmProjects\\pythonProject4\\gdp_growth_rate.csv', index=False)
vat.to_csv('C:\\Users\\danie\\PycharmProjects\\pythonProject4\\vat.csv', index=False)

# Display the first few rows of each DataFrame to verify
print(gdp_per_head.head())
print(population.head())
print(gdp_growth_rate.head())
print(vat.head())
