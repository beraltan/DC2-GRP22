import pandas as pd
import statsmodels.api as sm
from statsmodels.stats.outliers_influence import variance_inflation_factor

# Load the aggregated data
aggregated_file_path = 'aggregated_data_OutcomeCount_AvgScore.csv'
aggregated_df = pd.read_csv(aggregated_file_path)

# Prepare the data for regression analysis
outcomes_to_include = ['Outcome: Arrested', 'Outcome: Hospitalised', 'Outcome: Detained - Mental Health Act', 'Outcome: Other']
X = aggregated_df[outcomes_to_include]
y = aggregated_df['Average Score']

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
