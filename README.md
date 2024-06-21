# Impact of Use of Force on Public Trust and Confidence in the Metropolitan Police Service London

## Project Overview

This project examines the impact of the use of force on public trust and confidence in the Metropolitan Police Service (MPS) London. Using data from the Public Attitude Survey and the Use of Force dataset, the study applies various regression analyses to understand the relationships between the frequency and outcomes of use of force incidents, the subjects' age, and public perception.

### Conda Environment

First, create a conda environment using the provided `environment.yaml` file:

conda env create -n grp22 -f environment.yaml

create environment by ```conda env create =n grp22 -f environment.yaml```

activate the environmnt by `conda activate grp22`

Run the `data_loader.py` to obtain all the raw datasets

Then run  `preprocessing.py ` `data_Creation.py` `borough_trust.py` `ExportOutcomeAvgScoreValues.py` `futuredata.ipynb` `ImpactOnAvgScore.py`in order to pre-proccess the datasets

The python files are organized in folders regarding to their use case




## Table of Contents

- [Impact of Use of Force on Public Trust and Confidence in the Metropolitan Police Service London](#impact-of-use-of-force-on-public-trust-and-confidence-in-the-metropolitan-police-service-london)
  - [Project Overview](#project-overview)
    - [Conda Environment](#conda-environment)
  - [Table of Contents](#table-of-contents)
  - [Introduction](#introduction)
  - [Data Science Techniques](#data-science-techniques)
    - [Data Sources and Preparation](#data-sources-and-preparation)
    - [Regression Analysis](#regression-analysis)
  - [Addressing Sub-Research Questions](#addressing-sub-research-questions)
    - [Amount of Use of Force Cases](#amount-of-use-of-force-cases)
    - [Outcomes of Use of Force](#outcomes-of-use-of-force)
    - [Age Groups of Subjects](#age-groups-of-subjects)
  - [Forecasting Model and Dashboard](#forecasting-model-and-dashboard)
    - [Model Details](#model-details)
    - [Dashboard](#dashboard)
  - [Limitations and Future Work](#limitations-and-future-work)
  - [Conclusions and Recommendations](#conclusions-and-recommendations)
  - [Appendix](#appendix)

## Introduction

Trust and confidence in the police are essential for maintaining peace and order in communities. This report seeks to provide the MPS with insights and practical suggestions to foster a more trustworthy relationship with the public. By analyzing the Public Attitude Survey (PAS) and the Use of Force (UoF) datasets, we aim to identify key factors affecting public trust and confidence.

## Data Science Techniques

### Data Sources and Preparation

- **Public Attitude Survey (PAS):** Conducted by the Mayor’s Office for Policing And Crime (MOPAC) from December 31, 2014, to December 31, 2023. The dataset includes categories representing public perception, such as "Good Job" local, "Contact ward officer", "Informed local", "Listen to concerns", "Relied on to be there", "Treat everyone fairly", "Understand issues", and "Trust MPS".
- **Use of Force (UoF):** Conducted by the MPS from April 1, 2017, to May 31, 2024. This dataset includes columns like time, location, tactics used, and reason for force.

Data from the overlapping period (April 1, 2017, to December 31, 2023) was used for analysis, ensuring consistency in the time frame of the datasets.

### Regression Analysis

Ordinary Least Squares (OLS) regression was used to quantify the relationships between various factors and public trust and confidence. This method helps in understanding how different variables impact the average trust score.

## Addressing Sub-Research Questions

### Amount of Use of Force Cases

Analysis showed a statistically significant negative relationship between the number of use of force cases and public trust. A 1% increase in use of force cases is associated with a 0.000441 decrease in the average trust score.

### Outcomes of Use of Force

The analysis of outcomes like "Arrested", "Hospitalised", "Detained - Mental Health Act", and "Other" revealed varying impacts on trust. For instance, hospitalization incidents slightly increase trust, while arrests and detentions under the Mental Health Act decrease it.

### Age Groups of Subjects

Different age groups showed distinct impacts on trust. Use of force on subjects under 18 significantly decreases trust, while force used on subjects aged 18-34 slightly increases it.

## Forecasting Model and Dashboard

### Model Details

A random forest regression model was built to predict trust and confidence for the first quarter of 2024. The model explained approximately 50.48% of the variance in trust and confidence, with an R-squared value of 0.50480 and a mean absolute error of 0.03839.

### Dashboard

An interactive dashboard was developed to visualize predicted trust scores across London boroughs. This tool highlights changes in trust scores, providing actionable insights for the MPS.

## Limitations and Future Work

- **Sample Size:** Limited data spanning only 6 years and 3 quarters may affect model performance.
- **Accuracy of Use of Force Data:** Potential inaccuracies due to duplicate entries.
- **Categorization of Outcomes:** Further specification of "Other" outcomes could enhance analysis.
- **Age Group Classification:** Narrowing down age groups could reduce multicollinearity and improve insights.

Future work includes improving data recording practices, incorporating officer demographics, and refining age group classifications.

## Conclusions and Recommendations

More use of force cases, especially those resulting in arrests or detentions under the Mental Health Act, decrease public trust and confidence. Recommendations include investing in de-escalation training and avoiding use of force on subjects under 18 to improve public perception.

## Steps
1. Open the tools file and run the tool/data_creation.py to get all of the datasets. This will give you final_everything.csv
2. For each sub question, use the final_everything.csv
3. For sub question one, get the BoroughTrustNumOfCaseNEW.csv by running the tools/borough_trust.py
4. Once you have this file, all of the scripts under src/sub_questions/sq1 will be available to run the data through. These py files here include the visualizations and OLS model for sq1
5. For sub question 2, run the following py scripts to get the data needed for the codes refrenced: src/sub_questions/sq2/ExportOutcomeAvgScoreValues.py, src/sub_questions/sq2/NumberOfOutcomesBorough.py
6. Using the aggregated file created in ExportOutcomeAvgScoreValues.py u can run tools/ImpactOnAvgScore.py to get the final outcomes dataset needed for the visualizations
7. For subquestion 3 do the following: run src/sub_questions/sq3/OLS_subquestion3.py to get the OLS regression results for age groups
run src/sub_questions/getting_q4_2023_data.py to get the trust and confidence scores for the last quarter of 2023
run src/sub_questions/randomforest.py to run the forecasting model and output the predicted scores for the first quarter of 2024
8. For the dashboard three datasets are needed. These are new_trustALL_TIME.csv is -> (use: new_trust.csv this is provided when u run tool/data_creation.py) , futurescore2024.csv. Download the london_boroughs.geojson from this link: https://martinjc.github.io/UK-GeoJSON/
9. Use the datasets mentionaed above to run Dashboard/Predicted_Scores_Map.py
10. Then finally run Dashboard/Read.py to get the link to the dashboard


## Appendix

- [GitHub Repository](https://github.com/beraltan/DC2-GRP22)

Figures and additional details are available in the full technical report.

---

This README provides a structured overview of the project, highlighting key findings and recommendations. For detailed analysis and data visualizations, please refer to the full report in the repository.






