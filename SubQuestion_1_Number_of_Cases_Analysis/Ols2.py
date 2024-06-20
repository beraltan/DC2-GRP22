import numpy as np
import pandas as pd
import statsmodels.api as sm

# Load the dataset
file_path = 'BoroughTrustNumOfCaseNEW.csv'
data = pd.read_csv(file_path)

# Apply log transformation
data['Log_UseOfForceCount'] = np.log(data['UseOfForceCount'])

# Prepare the data for OLS regression
X = sm.add_constant(data['Log_UseOfForceCount'])
y = data['Average Score']

# Build the OLS model
model = sm.OLS(y, X).fit()

# Print the summary of the model
print(model.summary())
