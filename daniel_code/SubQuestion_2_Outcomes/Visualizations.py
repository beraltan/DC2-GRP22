import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Load the CSV file into a DataFrame
file_path = 'Final_Impact_of_Outcomes'  # Ensure your file path is correct
data = pd.read_csv(file_path)

# Calculate the mean of Total_Impact for each borough
mean_impact_per_borough = data.groupby('Borough')['Total_Impact'].mean().reset_index()

# Plot total impact by borough in descending order of mean impact
plt.figure(figsize=(14, 8))
ax = sns.barplot(x='Borough', y='Total_Impact', color='Blue', data=data, order=mean_impact_per_borough.sort_values('Total_Impact', ascending=False)['Borough'], ci=None)
plt.axhline(mean_impact_per_borough['Total_Impact'].mean(), color='red', linestyle='--', label=f'Mean: {mean_impact_per_borough["Total_Impact"].mean():.2f}')
plt.xticks(rotation=90)
plt.title('Impact on Average Score by Borough Based on SubQuestion_2_Outcomes')
plt.ylabel('Impact on Average Score')
plt.legend()
plt.tight_layout()  # Adjust layout to prevent label cutoff
plt.show()

# Transform the data for the stacked bar chart
impact_columns = ['Impact_Outcome: Arrested', 'Impact_Outcome: Hospitalised', 'Impact_Outcome: Detained - Mental Health Act', 'Impact_Outcome: Other']
data_long = data.melt(id_vars=['Borough'], value_vars=impact_columns, var_name='Outcome', value_name='Impact')

# Plot stacked bar chart of impact by outcome
plt.figure(figsize=(14, 8))
sns.barplot(x='Borough', y='Impact', hue='Outcome', data=data_long, ci=None)
plt.xticks(rotation=90)
plt.title('Impact on Average Score by Outcome and Borough')
plt.ylabel('Impact on Average Score')
plt.tight_layout()  # Adjust layout to prevent label cutoff
plt.show()
