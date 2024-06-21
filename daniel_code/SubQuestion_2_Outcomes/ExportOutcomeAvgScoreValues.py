import pandas as pd

# Load the merged data with all columns
merged_file_path = r'C:\Users\danie\PycharmProjects\DC2\qwe\final_everything.csv'
merged_df = pd.read_csv(merged_file_path, low_memory=False)

# Ensure the date columns are in datetime format
merged_df['IncidentDate'] = pd.to_datetime(merged_df['IncidentDate'])
merged_df['Date'] = pd.to_datetime(merged_df['Date'])

# Convert "yes"/"no" to 1/0 for all applicable columns
yes_no_columns = ['Outcome: Arrested', 'Outcome: Hospitalised',
                  'Outcome: Detained - Mental Health Act', 'Outcome: Other']

for col in yes_no_columns:
    merged_df[col] = merged_df[col].map({'Yes': 1, 'No': 0})

# Aggregate the number of use of force cases by Borough and Date
uof_counts = merged_df.groupby(['Borough', 'Date']).size().reset_index(name='UseOfForceCount')

# Aggregate outcome columns by Borough and Date
outcome_columns = yes_no_columns
outcome_aggregated = merged_df.groupby(['Borough', 'Date'])[outcome_columns].sum().reset_index()

# Merge the aggregated use of force data with the average score and outcome data
trust_scores = merged_df[['Borough', 'Date', 'Average Score']].drop_duplicates()
combined_df = pd.merge(uof_counts, trust_scores, on=['Borough', 'Date'])
combined_df = pd.merge(combined_df, outcome_aggregated, on=['Borough', 'Date'])

# Ensure all necessary columns are numeric and handle missing values
combined_df['Average Score'] = pd.to_numeric(combined_df['Average Score'], errors='coerce')

# Debugging: Check for NaNs before dropping
print("\nNaN Check Before Dropping:")
print(combined_df.isna().sum())

# Handle missing values
combined_df.dropna(inplace=True)

# Debugging: Check for empty columns after cleaning
print("\nEmpty Columns Check After Cleaning:")
print(combined_df.isnull().sum())

# Ensure there is valid data
if combined_df.empty:
    raise ValueError("The combined_df is empty after cleaning. Check the data preprocessing steps.")

# Export the aggregated data to CSV
output_file_path = r'aggregated_data_OutcomeCount_AvgScore.csv'
combined_df.to_csv(output_file_path, index=False)

print(f"Aggregated data exported to {output_file_path}")
