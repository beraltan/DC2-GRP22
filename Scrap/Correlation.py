import pandas as pd
import matplotlib.pyplot as plt

# Define the necessary columns to load
necessary_columns = ['IncidentDate', 'Borough']

# Load the combined use of force data with only the necessary columns
uof_file_path = '../qwe/FullUoFDC2.csv'
combined_uof_data = pd.read_csv(uof_file_path, usecols=necessary_columns, low_memory=False)

# Load the trust data
trust_file_path = '../qwe/trustDC2.csv'
trust_data = pd.read_csv(trust_file_path)

# Convert 'IncidentDate' to datetime
combined_uof_data['IncidentDate'] = pd.to_datetime(combined_uof_data['IncidentDate'], errors='coerce')

# Filter for records from July 2021 onwards
filtered_uof_data = combined_uof_data[combined_uof_data['IncidentDate'] >= '2021-07-01']

# Calculate the number of use of force incidents per borough
incidents_per_borough = filtered_uof_data.groupby('Borough').size().reset_index(name='IncidentCount')

# Merge with trust data
combined_data = pd.merge(incidents_per_borough, trust_data, on='Borough', how='inner')

# Calculate correlation
correlation = combined_data['IncidentCount'].corr(combined_data['Average Score'])
print(f"Correlation between number of incidents and trust score: {correlation}")

# Plot the data
plt.figure(figsize=(10, 6))
plt.scatter(combined_data['IncidentCount'], combined_data['Average Score'])
plt.title('Correlation between Use of Force Incidents and Trust Score (After July 2021)')
plt.xlabel('Number of Use of Force Incidents')
plt.ylabel('Trust Score')
plt.grid(True)
plt.tight_layout()
plt.show()
