import pandas as pd
import os




# Create output_files directory if it doesn't exist
output_dir = 'data/output_files'
os.makedirs(output_dir, exist_ok=True)

output_dir = 'data/output_files/output_pngs'
os.makedirs(output_dir, exist_ok=True)





gran = pd.read_excel('data/secondary_data/pas_data/PAS_T%26Cdashboard_to%20Q3%2023-24.xlsx', sheet_name='Borough')
gran = gran.drop(columns=['Unnamed: 9', 'Unnamed: 6', 'Unnamed: 7', 'Unnamed: 8', 'Survey'])

measure_list = list(gran['Measure'].unique())

for measure in measure_list:
    temp = gran[gran['Measure'] == measure]
    gran[measure] = temp['Proportion']

gran = gran.drop('Measure', axis=1)
gran = gran.drop('Proportion', axis=1)
gran = gran.drop('MPS', axis=1)

gran['Borough'] = gran['Borough'].replace(['Richmond Upon Thames'], ['Richmond upon Thames'])

gran = gran.groupby(['Date', 'Borough']).max().reset_index()

gran = gran.dropna()
gran['Average Score'] = gran.loc[:, '"Good Job" local':'Trust MPS'].mean(axis=1)
gran['Average Score'] = gran['Average Score'].round(4)
gran['Rank'] = gran.groupby('Date')['Average Score'].rank("dense", ascending=False)

gran.to_csv('data/output_files/new_trust.csv', index=False)

use1 = pd.read_excel('data/secondary_data/use_of_force/MPS Use of Force - FY24-25.xlsx')
use2 = pd.read_excel('data/secondary_data/use_of_force/MPS Use of Force - FY23-24.xlsx')
use3 = pd.read_excel('data/secondary_data/use_of_force/MPS Use of Force - FY22-23.xlsx')
use4 = pd.read_excel('data/secondary_data/use_of_force/MPS Use of Force - FY21-22.xlsx')
use5 = pd.read_excel('data/secondary_data/use_of_force/MPS Use of Force - FY20-21.xlsx')
use6 = pd.read_excel('data/secondary_data/use_of_force/MPS Use of Force - FY19-20.xlsx')
use7 = pd.read_excel('data/secondary_data/use_of_force/MPS Use of Force - FY18-19.xlsx')
use8 = pd.read_excel('data/secondary_data/use_of_force/MPS Use of Force - FY17-18.xlsx')

uof = pd.concat([use1, use2, use3, use4, use5, use6, use7, use8], axis=0, ignore_index=True)
uof.drop_duplicates(inplace=True)  # not number of incidents, each officer may enter the same data

date_list = list(gran['Date'].unique())
uof['IncidentDate'] = pd.to_datetime(uof['IncidentDate'])


def find_closest_future_date(initial_date, date_list):
    future_dates = [date for date in date_list if date > initial_date]
    if future_dates:
        return min(future_dates)
    else:
        return None

uof['Date'] = uof['IncidentDate'].apply(lambda x: find_closest_future_date(x, date_list))
uof = uof.dropna(subset=['Date'])
uof['Date'] = pd.to_datetime(uof['Date'])

uof.to_csv('data/output_files/new_uof.csv', index=False)

gran = gran[['Borough', 'Date', 'Average Score']]
df_merged = pd.merge(uof, gran, on=['Date', 'Borough'], how='left')
df_merged = df_merged.dropna(subset=['Average Score'])
df_merged.to_csv('data/output_files/final_everything.csv', index=False)
