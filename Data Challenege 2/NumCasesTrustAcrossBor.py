import pandas as pd

# Load the merged data
merged_file_path = '../qwe/everythingMerged.csv'
merged_df = pd.read_csv(merged_file_path)

# Ensure the date columns are in datetime format
merged_df['IncidentDate'] = pd.to_datetime(merged_df['IncidentDate'])
merged_df['Date'] = pd.to_datetime(merged_df['Date'])

# Aggregate the number of use of force cases by Borough and Date
uof_counts = merged_df.groupby(['Borough', 'Date']).size().reset_index(name='UseOfForceCount')

# Merge the aggregated use of force data with the average score
trust_scores = merged_df[['Borough', 'Date', 'Average Score']].drop_duplicates()
combined_df = pd.merge(uof_counts, trust_scores, on=['Borough', 'Date'])

# Calculate and print the correlation for each borough
boroughs = combined_df['Borough'].unique()

for borough in boroughs:
    borough_df = combined_df[combined_df['Borough'] == borough]
    correlation = borough_df['UseOfForceCount'].corr(borough_df['Average Score'])
    print(f"Borough: {borough}, Correlation: {correlation}")
