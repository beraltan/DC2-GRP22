import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from scipy.stats import pearsonr

# Load the merged data
merged_file_path = r'C:\Users\danie\PycharmProjects\DC2\qwe\everythingMerged.csv'
merged_df = pd.read_csv(merged_file_path, low_memory=False)

# Ensure the date columns are in datetime format
merged_df['IncidentDate'] = pd.to_datetime(merged_df['IncidentDate'])
merged_df['Date'] = pd.to_datetime(merged_df['Date'])

# Aggregate the number of use of force cases by Borough and Date
uof_counts = merged_df.groupby(['Borough', 'Date']).size().reset_index(name='UseOfForceCount')

# Merge the aggregated use of force data with the average score
trust_scores = merged_df[['Borough', 'Date', 'Average Score']].drop_duplicates()
combined_df = pd.merge(uof_counts, trust_scores, on=['Borough', 'Date'])

# Export the combined data to a CSV file
combined_df.to_csv('qwe/BoroughTrustNumOfCase.csv', index=False)

# Calculate and print the correlation for each borough
boroughs = combined_df['Borough'].unique()

correlation_results = []

for borough in boroughs:
    borough_df = combined_df[combined_df['Borough'] == borough]
    if len(borough_df) > 1:
        correlation, p_value = pearsonr(borough_df['UseOfForceCount'], borough_df['Average Score'])
        correlation_results.append((borough, correlation, p_value))
        print(f"Borough: {borough}, Correlation: {correlation}, P-value: {p_value}")
    else:
        print(f"Borough: {borough}, Not enough data to calculate correlation")

# Descriptive statistics
print("\nDescriptive Statistics:")
print(combined_df.describe())

# Visualizations
for borough in boroughs:
    borough_df = combined_df[combined_df['Borough'] == borough]
    if len(borough_df) > 1:
        sns.lmplot(x='UseOfForceCount', y='Average Score', data=borough_df, aspect=1.5)
        plt.title(f'Relationship between Use of Force Count and Average Trust Score in {borough}')
        plt.xlabel('Use of Force Count')
        plt.ylabel('Average Trust Score')
        plt.show()

# Correlation results
correlation_results_df = pd.DataFrame(correlation_results, columns=['Borough', 'Correlation', 'P-value'])
print("\nCorrelation Results:")
print(correlation_results_df)

# Check for multicollinearity
corr_matrix = combined_df.corr()
print("\nCorrelation Matrix:")
print(corr_matrix)
sns.heatmap(corr_matrix, annot=True, cmap='coolwarm')
plt.title('Correlation Matrix')
plt.show()
