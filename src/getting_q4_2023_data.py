import pandas as pd
import numpy as np

uof1 = pd.read_excel('data/secondary_data/use_of_force/MPS Use of Force - FY24-25.xlsx')
uof2 = pd.read_excel('data/secondary_data/use_of_force/MPS Use of Force - FY23-24.xlsx')

uof = pd.concat([uof1, uof2], ignore_index=True)
uof = uof[(uof['IncidentDate'] >= '2024-01-01') & (uof['IncidentDate'] < '2024-04-01')]

check = ['SubjectAge']
base = ['Borough']
outcome = [col for col in uof.columns if col.startswith('Outcome:')]
training = []

temp = uof[check+base+outcome]
grouped = temp.groupby(['Borough'])
total_counts = grouped.size()

underaged_counts = temp[(temp['SubjectAge'] == "0-10")|(temp['SubjectAge'] == "11-17")].groupby(['Borough']).size()
percent_underaged = (underaged_counts).reindex(grouped.indices, fill_value=0)
temp['Under18'] = temp.set_index(['Borough']).index.map(percent_underaged)
training.append('Under18')

underaged_counts = temp[(temp['SubjectAge'] == "18-34")].groupby(['Borough']).size()
percent_underaged = (underaged_counts).reindex(grouped.indices, fill_value=0)
temp['Age18to34'] = temp.set_index(['Borough']).index.map(percent_underaged)
training.append('Age18to34')

underaged_counts = temp[(temp['SubjectAge'] == "35-49")].groupby(['Borough']).size()
percent_underaged = (underaged_counts).reindex(grouped.indices, fill_value=0)
temp['Age35to49'] = temp.set_index(['Borough']).index.map(percent_underaged)
training.append('Age35to49')

over50_counts = temp[(temp['SubjectAge'] == "50-64")|(temp['SubjectAge'] == "65 and over")].groupby(['Borough']).size()
percent_over50 = (over50_counts).reindex(grouped.indices, fill_value=0)
temp['Over50'] = temp.set_index(['Borough']).index.map(percent_over50)
training.append('Over50')

over50_counts = temp[(temp['SubjectAge'] == "50-64")|(temp['SubjectAge'] == "65 and over")].groupby(['Borough']).size()
percent_over50 = (over50_counts).reindex(grouped.indices, fill_value=0)
temp['Over50'] = temp.set_index(['Borough']).index.map(percent_over50)
training.append('Over50')

firearmsaimed_counts = temp[(temp['Outcome: Arrested'] == "Yes")].groupby(['Borough']).size()
percent_firearmsaimed = (firearmsaimed_counts).reindex(grouped.indices, fill_value=0)
temp['Arrested'] = temp.set_index(['Borough']).index.map(percent_firearmsaimed)
training.append('Arrested')

firearmsaimed_counts = temp[(temp['Outcome: Hospitalised'] == "Yes")].groupby(['Borough']).size()
percent_firearmsaimed = (firearmsaimed_counts).reindex(grouped.indices, fill_value=0)
temp['Hospitalised'] = temp.set_index(['Borough']).index.map(percent_firearmsaimed)
training.append('Hospitalised')

firearmsaimed_counts = temp[(temp['Outcome: Detained - Mental Health Act'] == "Yes")].groupby(['Borough']).size()
percent_firearmsaimed = (firearmsaimed_counts).reindex(grouped.indices, fill_value=0)
temp['DetainedMHA'] = temp.set_index(['Borough']).index.map(percent_firearmsaimed)
training.append('DetainedMHA')

firearmsaimed_counts = temp[(temp['Outcome: Other'] == "Yes")].groupby(['Borough']).size()
percent_firearmsaimed = (firearmsaimed_counts).reindex(grouped.indices, fill_value=0)
temp['Other'] = temp.set_index(['Borough']).index.map(percent_firearmsaimed)
training.append('Other')

temp['UoF Cases'] = temp.groupby(['Borough'])['Borough'].transform('count')
temp['Log of UoF Cases'] = np.log(temp['UoF Cases'])
training.append('Log of UoF Cases')

temp = temp.drop(columns=(check+outcome))
temp = temp.drop(columns=['UoF Cases'])
temp = temp.fillna(0)
temp.drop_duplicates(inplace=True)
temp = temp.reset_index()
temp = temp.drop(columns=['index'])

temp.to_csv('data/output_files/predict.csv', index=False)