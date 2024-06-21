import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import GridSearchCV
from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score
from sklearn import metrics

uof = pd.read_csv('final_everything.csv')

check = ['SubjectAge']
base = ['Borough', 'Average Score', 'Date']
outcome = [col for col in uof.columns if col.startswith('Outcome:')]
training = []

temp = uof[check+base+outcome]
grouped = temp.groupby(['Borough', 'Date'])
total_counts = grouped.size()

underaged_counts = temp[(temp['SubjectAge'] == "0-10")|(temp['SubjectAge'] == "11-17")].groupby(['Borough', 'Date']).size()
percent_underaged = (underaged_counts).reindex(grouped.indices, fill_value=0)
temp['Under18'] = temp.set_index(['Borough', 'Date']).index.map(percent_underaged)
training.append('Under18')

underaged_counts = temp[(temp['SubjectAge'] == "18-34")].groupby(['Borough', 'Date']).size()
percent_underaged = (underaged_counts).reindex(grouped.indices, fill_value=0)
temp['Age18to34'] = temp.set_index(['Borough', 'Date']).index.map(percent_underaged)
training.append('Age18to34')

underaged_counts = temp[(temp['SubjectAge'] == "35-49")].groupby(['Borough', 'Date']).size()
percent_underaged = (underaged_counts).reindex(grouped.indices, fill_value=0)
temp['Age35to49'] = temp.set_index(['Borough', 'Date']).index.map(percent_underaged)
training.append('Age35to49')

over50_counts = temp[(temp['SubjectAge'] == "50-64")|(temp['SubjectAge'] == "65 and over")].groupby(['Borough', 'Date']).size()
percent_over50 = (over50_counts).reindex(grouped.indices, fill_value=0)
temp['Over50'] = temp.set_index(['Borough', 'Date']).index.map(percent_over50)
training.append('Over50')

over50_counts = temp[(temp['SubjectAge'] == "50-64")|(temp['SubjectAge'] == "65 and over")].groupby(['Borough', 'Date']).size()
percent_over50 = (over50_counts).reindex(grouped.indices, fill_value=0)
temp['Over50'] = temp.set_index(['Borough', 'Date']).index.map(percent_over50)
training.append('Over50')

firearmsaimed_counts = temp[(temp['Outcome: Arrested'] == "Yes")].groupby(['Borough', 'Date']).size()
percent_firearmsaimed = (firearmsaimed_counts).reindex(grouped.indices, fill_value=0)
temp['Arrested'] = temp.set_index(['Borough', 'Date']).index.map(percent_firearmsaimed)
training.append('Arrested')

firearmsaimed_counts = temp[(temp['Outcome: Hospitalised'] == "Yes")].groupby(['Borough', 'Date']).size()
percent_firearmsaimed = (firearmsaimed_counts).reindex(grouped.indices, fill_value=0)
temp['Hospitalised'] = temp.set_index(['Borough', 'Date']).index.map(percent_firearmsaimed)
training.append('Hospitalised')

firearmsaimed_counts = temp[(temp['Outcome: Detained - Mental Health Act'] == "Yes")].groupby(['Borough', 'Date']).size()
percent_firearmsaimed = (firearmsaimed_counts).reindex(grouped.indices, fill_value=0)
temp['DetainedMHA'] = temp.set_index(['Borough', 'Date']).index.map(percent_firearmsaimed)
training.append('DetainedMHA')

firearmsaimed_counts = temp[(temp['Outcome: Other'] == "Yes")].groupby(['Borough', 'Date']).size()
percent_firearmsaimed = (firearmsaimed_counts).reindex(grouped.indices, fill_value=0)
temp['Other'] = temp.set_index(['Borough', 'Date']).index.map(percent_firearmsaimed)
training.append('Other')

temp['UoF Cases'] = temp.groupby(['Date', 'Borough'])['Borough'].transform('count')
temp['Log of UoF Cases'] = np.log(temp['UoF Cases'])
training.append('Log of UoF Cases')

temp = temp.drop(columns=(check+outcome))
temp = temp.drop(columns=['Date'])
temp = temp.drop(columns=['Borough'])
temp = temp.drop(columns=['UoF Cases'])
temp = temp.fillna(0)
temp.drop_duplicates(inplace=True)

X = temp.drop('Average Score',axis=1)
y = temp['Average Score']

# 70% training data
X_train, X_temp, y_train, y_temp = train_test_split(X, y, train_size=0.7, random_state=42)

# 15% for test and val
X_val, X_test, y_val, y_test = train_test_split(X_temp, y_temp, test_size=0.5, random_state=42)

rf_params = {
    'n_estimators': [50, 100, 150, 200, 250, 300, 350, 400, 450, 500],
    'max_features': ['log2', 'sqrt', None],
    'max_depth': [2, 3, 4, 5, 6, 7, 8, 9, 10]
}

rf = RandomForestRegressor(random_state=42)
grid_search = GridSearchCV(rf, rf_params, cv=5)

grid_search.fit(X_train, y_train)

print(grid_search.best_params_)
print(grid_search.best_score_)

forest = RandomForestRegressor(**grid_search.best_params_, random_state=0)
forest.fit(X_train, y_train)

y_val_pred = forest.predict(X_val)

val_mse = mean_squared_error(y_val, y_val_pred)
val_mae = mean_absolute_error(y_val, y_val_pred)
val_r2 = r2_score(y_val, y_val_pred)

print("Validation MSE:", val_mse)
print("Validation MAE:", val_mae)
print("Validation R² Score:", val_r2)

y_pred = forest.predict(X_test)

mape = np.mean(np.abs((y_test - y_pred) / np.abs(y_test)))
print('Mean Absolute Percentage Error (MAPE):', round(mape * 100, 2))
print('Accuracy:', round(100*(1 - mape), 2))
print('Mean Absolute Error (MAE):', metrics.mean_absolute_error(y_test, y_pred))
print('Mean Squared Error (MSE):', metrics.mean_squared_error(y_test, y_pred))
print('Root Mean Squared Error (RMSE):', metrics.mean_squared_error(y_test, y_pred, squared=False))
print('Mean Absolute Percentage Error (MAPE):', metrics.mean_absolute_percentage_error(y_test, y_pred))
print('Explained Variance Score:', metrics.explained_variance_score(y_test, y_pred))
print('Max Error:', metrics.max_error(y_test, y_pred))
print('Median Absolute Error:', metrics.median_absolute_error(y_test, y_pred))
print('R^2:', metrics.r2_score(y_test, y_pred))
print('Mean Poisson Deviance:', metrics.mean_poisson_deviance(y_test, y_pred))
print('Mean Gamma Deviance:', metrics.mean_gamma_deviance(y_test, y_pred))

predict = pd.read_csv('predict.csv')
no_borough = predict.copy()
no_borough = no_borough.drop(columns='Borough')
new_predictions = forest.predict(no_borough)

predict['Average Score'] = new_predictions
predict.to_csv('futurescore.csv', index=False)
df = predict[['Borough', 'Average Score']]
df = df.sort_values(by='Average Score', ascending=False).reset_index(drop=True)
df['Rank'] = df['Average Score'].rank(method='min', ascending=False).astype(int)

trend = pd.read_csv('new_trust.csv')
trend = trend[trend['Date'] > '2023-10-31']
trend = trend[['Average Score', 'Rank', 'Borough']]
merged_df = pd.merge(df, trend, on=['Borough'],how='left')
merged_df.rename(columns={'Average Score_x': 'Last Average Score', 'Average Score_y': 'New Average Score', 'Rank_x': 'Last Rank', 'Rank_y': 'New Rank'}, inplace=True)
merged_df['Rank Change'] = merged_df['New Rank'] - merged_df['Last Rank']
merged_df['Score Change'] = merged_df['New Average Score'] - merged_df['Last Average Score']
merged_df.head(30)
