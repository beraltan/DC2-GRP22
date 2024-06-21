import pandas as pd
import xgboost as xgb
from sklearn.model_selection import train_test_split
import matplotlib.pyplot as plt
from sklearn.preprocessing import LabelEncoder


def process_csv(file_path, output_path):
    # Load the dataset
    data = pd.read_csv(file_path)

    # Drop columns that are fully empty
    cleaned_data = data.dropna(axis=1, how='all')

    # Identify categorical columns in the cleaned data
    categorical_cols = cleaned_data.select_dtypes(include=['object']).columns

    # Initialize a label encoder for each categorical column in the cleaned data
    label_encoders = {col: LabelEncoder() for col in categorical_cols}

    # Apply label encoding to each categorical column in the cleaned data
    for col, le in label_encoders.items():
        cleaned_data[col] = le.fit_transform(cleaned_data[col].astype(str))

    # Drop columns where all values are 0
    columns_to_drop = [col for col in cleaned_data.columns if
                       cleaned_data[col].nunique() == 1 and cleaned_data[col].unique()[0] == 0]
    final_cleaned_data = cleaned_data.drop(columns=columns_to_drop)

    # Save the cleaned and encoded dataframe to a new CSV file
    final_cleaned_data.to_csv(output_path, index=False)

process_csv('../qwe/everythingMerged.csv', 'qwe/Everythingxg.csv')