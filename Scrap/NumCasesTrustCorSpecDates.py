import pandas as pd

# Load the merged data
merged_file_path = '../qwe/everythingMerged.csv'  # Replace with your actual file path
merged_df = pd.read_csv(merged_file_path, low_memory=False)

# Ensure the date columns are in datetime format
merged_df['IncidentDate'] = pd.to_datetime(merged_df['IncidentDate'])
merged_df['Date'] = pd.to_datetime(merged_df['Date'])

# Check for any potential issues in the data
print("Data Info:")
print(merged_df.info())
print("\nFirst few rows of the data:")
print(merged_df.head())

# Filter data for the period from January 2023 to March 2024
start_date = '2020-01-01'
end_date = '2021-01-01'
filtered_df = merged_df[(merged_df['IncidentDate'] >= start_date) & (merged_df['IncidentDate'] <= end_date)]

# Ensure that the data is sorted by Borough and IncidentDate
filtered_df.sort_values(by=['Borough', 'IncidentDate'], inplace=True)

# Aggregate the number of use of force cases by Borough and Date
uof_counts = filtered_df.groupby(['Borough', 'Date']).size().reset_index(name='UseOfForceCount')

# Merge the aggregated use of force data with the average score
trust_scores = filtered_df[['Borough', 'Date', 'Average Score']].drop_duplicates()
combined_df = pd.merge(uof_counts, trust_scores, on=['Borough', 'Date'])

# Check for any potential issues in the combined data
print("\nCombined Data Info:")
print(combined_df.info())
print("\nFirst few rows of the combined data:")
print(combined_df.head())

# Calculate and print the correlation for each borough for the filtered period
boroughs = combined_df['Borough'].unique()

print("\nCorrelation from January 2022 to January 2023:")
for borough in boroughs:
    borough_df = combined_df[combined_df['Borough'] == borough]
    if len(borough_df) > 1:  # Ensure there is enough data to calculate correlation
        correlation = borough_df['UseOfForceCount'].corr(borough_df['Average Score'])
        print(f"Borough: {borough}, Correlation: {correlation}")
    else:
        print(f"Borough: {borough}, Not enough data to calculate correlation")
