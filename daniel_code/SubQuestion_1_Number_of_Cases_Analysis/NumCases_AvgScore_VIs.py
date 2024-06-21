import matplotlib.pyplot as plt
import pandas as pd
from sklearn.preprocessing import MinMaxScaler

# Load the data
file_path = 'BoroughTrustNumOfCaseNEW.csv'
data = pd.read_csv(file_path)

# Convert the 'Date' column to datetime format
data['Date'] = pd.to_datetime(data['Date'])

# Group by 'Date' and sum the 'UseOfForceCount' for all boroughs, and mean the 'Average Score'
use_of_force_group = data.groupby('Date')['UseOfForceCount'].sum()
average_score_group = data.groupby('Date')['Average Score'].mean()

# Normalize the data
scaler = MinMaxScaler()
use_of_force_scaled = scaler.fit_transform(use_of_force_group.values.reshape(-1, 1))
average_score_scaled = scaler.fit_transform(average_score_group.values.reshape(-1, 1))

# Plot the data
plt.figure(figsize=(8, 5))
plt.plot(use_of_force_group.index, use_of_force_scaled, marker='o', label='Total Use of Force Cases (Normalized)')
plt.plot(average_score_group.index, average_score_scaled, marker='o', label='Mean Average Score of All Boroughs (Normalized)')

# Set title and labels
plt.title("Total Use of Force Cases and Mean Average Score per Survey Date (Normalized)")
plt.xlabel("Date")
plt.ylabel("Normalized Values")
plt.grid(True)
plt.xticks(rotation=90)

# Add legend and adjust layout
plt.legend()
plt.tight_layout()

# Save and show the plot
plt.savefig("total_use_of_force_cases_and_average_score_per_survey_date_normalized.png")
plt.show()
