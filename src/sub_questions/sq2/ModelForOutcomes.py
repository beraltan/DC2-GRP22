import pandas as pd
import statsmodels.api as sm
from statsmodels.stats.outliers_influence import variance_inflation_factor

# Load the merged data with all columns
merged_file_path = 'data/output_files/final_everything.csv'
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

# Prepare the data for regression analysis
# Exclude 'Outcome: Made off/escaped' and 'Outcome: Fatality' as they are no longer recorded
outcomes_to_include = [col for col in outcome_columns if col not in ['Outcome: Made off/escaped', 'Outcome: Fatality']]
# Remove 'UseOfForceCount'
X = combined_df[outcomes_to_include]
y = combined_df['Average Score']

# Add a constant to the independent variables matrix
X = sm.add_constant(X)

# Fit the regression model
model = sm.OLS(y, X).fit()

# Print the regression results
print(model.summary())

# Recalculate VIF
vif_data = pd.DataFrame()
vif_data["Variable"] = X.columns
vif_data["VIF"] = [variance_inflation_factor(X.values, i) for i in range(len(X.columns))]

print("\nVariance Inflation Factor (VIF):")
print(vif_data)
