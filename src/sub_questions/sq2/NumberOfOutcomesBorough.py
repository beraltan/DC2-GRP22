import pandas as pd

# Load the merged data with all columns
merged_file_path = 'data/output_files/final_everything.csv'

merged_df = pd.read_csv(merged_file_path, low_memory=False)

# Ensure the date columns are in datetime format
merged_df['IncidentDate'] = pd.to_datetime(merged_df['IncidentDate'])
merged_df['Date'] = pd.to_datetime(merged_df['Date'])

# Extract year from the date
merged_df['Year'] = merged_df['Date'].dt.year

# Convert "Yes"/"No" to 1/0 for all applicable columns
yes_no_columns = ['SubjectInjured', 'Outcome: Arrested', 'Outcome: Hospitalised',
                  'Outcome: Detained - Mental Health Act', 'Outcome: Other']

for col in yes_no_columns:
    merged_df[col] = merged_df[col].map({'Yes': 1, 'No': 0})

# Group by Borough and Year, then calculate the average number of cases for each outcome
average_outcomes_per_year = merged_df.groupby(['Borough', 'Year'])[yes_no_columns].sum().groupby(
    'Borough').mean().reset_index()

# Print the result
print(average_outcomes_per_year)

# Save the result to a CSV file if needed
average_outcomes_per_year.to_csv('data/output_files/average_outcomes_per_yearNEW.csv', index=False)
