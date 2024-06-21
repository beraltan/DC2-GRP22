import pandas as pd
import matplotlib.pyplot as plt
import statsmodels.api as sm
from statsmodels.stats.outliers_influence import variance_inflation_factor
from sklearn.linear_model import Ridge, Lasso

uof = pd.read_csv('final_everything.csv')
uof.loc[uof.SubjectEthnicity == 'Chinese', 'SubjectEthnicity'] = 'Asian (or Asian British)'
uof = uof[uof['SubjectAge'] != '2017-11-01 00:00:00']

check = ['SubjectAge']
base = ['Borough', 'Average Score', 'Date']
training = []

temp = uof[check+base]
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

temp = temp.drop(columns=(check))
temp = temp.fillna(0)
temp.drop_duplicates(inplace=True)

X = temp[training]
y = temp['Average Score']

X = sm.add_constant(X)

VIF_df = pd.DataFrame()
VIF_df["Variable"] = X.columns
VIF_df["VIF"] = [variance_inflation_factor(X.values, i) for i in range(X.shape[1])]
print(VIF_df)

lasso = Lasso(alpha=0.05)  # Alpha value needs tuning
lasso.fit(X, y)

# Output coefficients
print("Coefficients:", lasso.coef_)

model = sm.OLS(y, X).fit()
print(model.summary())

temp = temp.drop(columns='Date')
temp_mean = temp.groupby('Borough').transform('mean')
temp.update(temp_mean)
temp = temp.drop_duplicates()
temp = temp.reset_index(drop=True)
temp.head(40)

coefficients = {
    'Under18': -0.0006,
    'Age18to34': 0.0002,
    'Age35to49': -0.0003,
    'Over50': -0.0003
}

temp['Impact'] = (
    coefficients['Under18'] * temp['Under18'] +
    coefficients['Age18to34'] * temp['Age18to34'] +
    coefficients['Age35to49'] * temp['Age35to49'] +
    coefficients['Over50'] * temp['Over50']
)

temp_sorted = temp.sort_values(by='Impact', ascending=False)

mean_impact = temp['Impact'].mean()

plt.figure(figsize=(14, 8))
plt.bar(temp_sorted['Borough'], temp_sorted['Impact'])
plt.axhline(mean_impact, color='r', linestyle='--', linewidth=1, label=f'Mean Impact: {mean_impact:.4f}')
plt.xticks(rotation=90)
plt.xlabel('Borough')
plt.ylabel('Impact on Average Score')
plt.title("Impact on Average Score per Borough Based on their Average Subjects' Age Groups")
plt.legend()
plt.tight_layout()
plt.savefig("Impact on Average Score Age.png")
plt.show()
