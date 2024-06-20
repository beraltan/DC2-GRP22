import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import numpy as np
import statsmodels.api as sm

# Load the dataset
file_path = 'BoroughTrustNumOfCaseNEW.csv'
data = pd.read_csv(file_path)

# Apply log transformation to UseOfForceCount
data['Log_UseOfForceCount'] = np.log1p(data['UseOfForceCount'])

# Prepare the data for OLS regression
X = sm.add_constant(data['Log_UseOfForceCount'])
y = data['Average Score']

# Build the OLS model
model = sm.OLS(y, X).fit()

# Calculate the residuals
data['Residuals'] = model.resid

# Plot the residuals
plt.figure(figsize=(12, 6))
sns.scatterplot(x=model.fittedvalues, y=data['Residuals'])
plt.axhline(0, color='red', linestyle='--')
plt.title('Residuals vs Fitted Values')
plt.xlabel('Fitted Values')
plt.ylabel('Residuals')
plt.show()
