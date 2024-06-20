import pandas as pd
import matplotlib.pyplot as plt

# Load the data from the provided Excel file
file_path = 'USE2-April23-Mar24.xlsx'

# Load both sheets
use_of_force_cases = pd.read_excel(file_path, sheet_name='UoF')
use_of_force_details = pd.read_excel(file_path, sheet_name='UoFPO')

# Display the first few rows of the data to understand its structure
print("UoF Data:")
print(use_of_force_cases.head())
print("UoFPO Data:")
print(use_of_force_details.head())

# Combine date and time columns to create a datetime index
use_of_force_cases['DateTime'] = pd.to_datetime(use_of_force_cases['IncidentDate'] + ' ' + use_of_force_cases['IncidentTime'])
use_of_force_details['DateTime'] = pd.to_datetime(use_of_force_details['IncidentDateStarted'].astype(str) + ' ' + use_of_force_details['IncidentStartTime'].astype(str))

# Display the first few rows to verify
print("UoF Data with DateTime:")
print(use_of_force_cases[['DateTime', 'Borough']].head())
print("UoFPO Data with DateTime:")
print(use_of_force_details[['DateTime', 'NoOfPeople']].head())

# Identify additional matching variables and merge datasets on DateTime and other common attributes
common_columns = ['DateTime', 'Tactic 1']  # Adjust based on the actual available columns

# Merge datasets
merged_data = pd.merge(use_of_force_cases, use_of_force_details, on=common_columns, how='inner')

# Display the merged data
print("Merged Data:")
print(merged_data.head())

# Define the categories for the number of people involved
people_categories = ['1 person', '2-5 people', '6-10 people', 'more than 10 people']

# Map NoOfPeople to the correct categories
merged_data['People_Category'] = pd.Categorical(merged_data['NoOfPeople'], categories=people_categories, ordered=True)

# Summarize the data
people_involved_summary = merged_data.groupby(['Borough', 'People_Category']).size().unstack(fill_value=0)

# Calculate the total number of cases per borough
total_cases_per_borough = people_involved_summary.sum(axis=1)

# Normalize the data by dividing each category count by the total number of cases in the borough
normalized_data = people_involved_summary.divide(total_cases_per_borough, axis=0)

# Plotting the normalized stacked bar chart
normalized_data.plot(kind='bar', stacked=True, figsize=(14, 7))
plt.title('Proportion of People Involved in Use of Force Cases by Borough')
plt.xlabel('Borough')
plt.ylabel('Proportion of Cases')
plt.xticks(rotation=90)
plt.legend(title='People Involved')
plt.tight_layout()
plt.show()
