import pandas as pd
import matplotlib.pyplot as plt

# Load only necessary columns from the Excel file
use_of_force_cases_columns = ['Borough', 'Firearms Aimed', 'Firearms Fired']
# use_of_force_details_columns = ['Date', 'Time', 'Number of People Involved']

file_path = 'USE2-April23-Mar24.xlsx'

# Load both sheets with only necessary columns
use_of_force_cases = pd.read_excel(file_path, sheet_name='UoF', usecols=use_of_force_cases_columns)
# use_of_force_details = pd.read_excel(file_path, sheet_name='UoFPO', usecols=use_of_force_details_columns)

# Display the first few rows of the data to understand its structure
print("UoF Data:")
print(use_of_force_cases.head())
# print("UoFPO Data:")
# print(use_of_force_details.head())

# Count occurrences of "yes" for Firearms Aimed and Firearms Fired for each borough
firearms_aimed_count = use_of_force_cases[use_of_force_cases['Firearms Aimed'] == 'Yes'].groupby('Borough').size()
firearms_fired_count = use_of_force_cases[use_of_force_cases['Firearms Fired'] == 'Yes'].groupby('Borough').size()

# Create a DataFrame for plotting
firearms_data = pd.DataFrame({'Firearms Aimed': firearms_aimed_count, 'Firearms Fired': firearms_fired_count})

# Fill NaN values with 0 (in case some boroughs have no counts for one of the categories)
firearms_data = firearms_data.fillna(0)

# Check the data to be plotted
print("Firearms Data to be plotted:")
print(firearms_data)

# Plotting the bar chart only if the DataFrame is not empty
if not firearms_data.empty:
    firearms_data.plot(kind='bar', figsize=(14, 7))
    plt.title('Firearms Aimed and Fired by Borough')
    plt.xlabel('Borough')
    plt.ylabel('Number of Occurrences')
    plt.xticks(rotation=0)
    plt.tight_layout()
    plt.show()
else:
    print("No data available to plot.")
