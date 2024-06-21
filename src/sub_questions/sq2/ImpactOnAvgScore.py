import pandas as pd

# Load the existing CSV file with aggregated data
aggregated_file_path = 'aggregated_data_OutcomeCount_AvgScore.csv'
aggregated_df = pd.read_csv(aggregated_file_path)

# Coefficients from the updated regression model
coefficients = {
    'Outcome: Arrested': -5.579e-05,
    'Outcome: Hospitalised': 0.0004,
    'Outcome: Detained - Mental Health Act': -0.0014,
    'Outcome: Other': 0.0003
}

# Calculate the impact on the Average Score for each borough
for outcome in coefficients.keys():
    aggregated_df[f'Impact_{outcome}'] = aggregated_df[outcome] * coefficients[outcome]

# Sum the impacts to get the total impact on the Average Score for each borough
aggregated_df['Total_Impact'] = aggregated_df[[f'Impact_{outcome}' for outcome in coefficients.keys()]].sum(axis=1)

# Print the result
print(aggregated_df[['Borough'] + [f'Impact_{outcome}' for outcome in coefficients.keys()] + ['Total_Impact']])

# Save the result to a new CSV file
output_file_path = 'data/output_files/Final_Impact_of_Outcomes.csv'
aggregated_df.to_csv(output_file_path, index=False)
print(f"Results exported to {output_file_path}")
