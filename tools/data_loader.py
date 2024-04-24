import requests
import os
import zipfile

import pandas as pd


def download_and_unzip(url, relative_path):
    # Navigate to the parent directory of the current script
    parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

    # Define the full path to the data folder
    data_folder = os.path.join(parent_dir, relative_path)

    # Ensure the folder exists
    if not os.path.exists(data_folder):
        os.makedirs(data_folder)

    # Define the path for the zip file
    zip_path = os.path.join(data_folder, "data.zip")
    
    # Download the file
    print("Downloading the file...")
    response = requests.get(url)
    with open(zip_path, 'wb') as file:
        file.write(response.content)
    print("Download completed.")

    # Unzip the file
    print("Unzipping the file...")
    with zipfile.ZipFile(zip_path, 'r') as zip_ref:
        zip_ref.extractall(data_folder)
    print("Unzipping completed.")

    # Optionally, remove the zip file after extraction
    os.remove(zip_path)
    print("Zip file removed.")

# Usage


url ="https://policeuk-data.s3.amazonaws.com/download/6cf8efbca9e6d7b14f23f0cb6e84afd30fe35fde.zip"
# url = "https://policeuk-data.s3.amazonaws.com/download/d14653c3a332b4238b9a419afe4a66d8bee6541e.zip"
download_and_unzip(url,"data/primary_data")




import os
import requests
import pandas as pd

def download_and_convert_excel_to_csv(url, output_dir, output_filename):
    try:
        # Ensure the output directory exists
        os.makedirs(output_dir, exist_ok=True)
        
        # Define the path for the downloaded Excel file
        excel_path = os.path.join(output_dir, output_filename + ".xlsx")
        
        # Download the file
        print("Downloading the Excel file...")
        response = requests.get(url)
        if response.status_code == 200:
            with open(excel_path, 'wb') as file:
                file.write(response.content)
            print("Download complete.")
        else:
            print(f"Failed to download the file. Status code: {response.status_code}")
            return
        
        # Load the downloaded Excel file
        print("Loading Excel file...")
        xls = pd.ExcelFile(excel_path)

        # Iterate through each sheet in the Excel file
        for sheet_name in xls.sheet_names:
            print(f"Processing sheet: {sheet_name}")
            df = pd.read_excel(xls, sheet_name=sheet_name)
            # Define path for the CSV output
            csv_path = os.path.join(output_dir, f"{output_filename}_{sheet_name}.csv")
            # Save the DataFrame as a CSV file
            df.to_csv(csv_path, index=False)
            print(f"Sheet {sheet_name} converted and saved as {csv_path}")

        # Optional: Remove the Excel file after conversion
        os.remove(excel_path)
        print("Excel file removed after conversion.")

    except Exception as e:
        print(f"An error occurred: {e}")

# URL of the Excel file
url = "https://data.london.gov.uk/download/earnings-place-residence-borough/1686ef1c-b169-442d-8877-e7e49788f668/earnings-residence-borough.xlsx"

# Call the function with the specified parameters
download_and_convert_excel_to_csv(url, "data/secondary_data", "earnings_residence_borough")


url = "https://policeuk-data.s3.amazonaws.com/download/d14653c3a332b4238b9a419afe4a66d8bee6541e.zip"
download_and_unzip(url, "data")

