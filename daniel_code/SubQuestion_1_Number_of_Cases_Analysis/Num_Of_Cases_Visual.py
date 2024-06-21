import matplotlib.pyplot as plt
import pandas as pd

# Load the data
file_path = 'BoroughTrustNumOfCaseNEW.csv'
data = pd.read_csv(file_path)

# Convert the 'Date' column to datetime format
data['Date'] = pd.to_datetime(data['Date'])

# Group by 'Date' and sum the 'UseOfForceCount' for all boroughs
date_group = data.groupby('Date')['UseOfForceCount'].sum()
date_group = date_group.sort_index()

# Plot the data
plt.figure(figsize=(8, 5))
plt.plot(date_group.index, date_group.values, marker='o', label='Total Use of Force Cases')

# Set title and labels
plt.title("Total Use of Force Cases per Survey Date")
plt.xlabel("Date")
plt.ylabel("Total Use of Force Cases")
plt.grid(True)
plt.xticks(date_group.index, date_group.index.strftime('%Y-%m-%d'), rotation=90)

# Add legend and adjust layout
plt.legend()
plt.tight_layout()

# Save and show the plot
plt.savefig("total_use_of_force_cases_per_survey_date.png")
plt.show()
