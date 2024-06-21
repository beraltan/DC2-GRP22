import pandas as pd
import statsmodels.api as sm
from statsmodels.stats.outliers_influence import variance_inflation_factor

path = "data/output_files/BoroughTrustNumOfCaseNEW.csv"
combined_df = pd.read_csv(path)
merged_file_path = r"C:\Users\danie\PycharmProjects\DC2\qwe\final_everything.csv"
merged_df = pd.read_csv(merged_file_path, low_memory=False)# Prepare the data for regression analysis
X = combined_df[['UseOfForceCount']]
y = combined_df['Average Score']

# Add a constant to the independent variables matrix
X = sm.add_constant(X)

# Fit the regression model
model = sm.OLS(y, X).fit()

# Print the regression results
print(model.summary())

# # Check for multicollinearity using VIF
# # Add the other potential predictors to X here
# X['SubjectAge'] = merged_df['SubjectAge']
# X['Tactic 1'] = merged_df['Tactic 1']
# X['PrimaryConduct'] = merged_df['PrimaryConduct']
#
# # Calculate VIF for each predictor
# vif_data = pd.DataFrame()
# vif_data["Variable"] = X.columns
# vif_data["VIF"] = [variance_inflation_factor(X.values, i) for i in range(len(X.columns))]
#
# print("\nVariance Inflation Factor (VIF):")
# print(vif_data)
