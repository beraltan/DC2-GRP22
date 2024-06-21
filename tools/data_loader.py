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


url ="https://policeuk-data.s3.amazonaws.com/download/bc01a9eeaca07ca2a833387849b7cab7e2ee06fa.zip"
# url = "https://policeuk-data.s3.amazonaws.com/download/d14653c3a332b4238b9a419afe4a66d8bee6541e.zip"
download_and_unzip(url,"data/primary_data")








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
url2  = 'https://data.london.gov.uk/download/lsoa-atlas/b8e01c3a-f5e3-4417-82b3-02ad271e6ee8/lsoa-data.xls'

# Call the function with the specified parameters
download_and_convert_excel_to_csv(url, "data/secondary_data/income_by_region", "earnings_residence_borough")
download_and_convert_excel_to_csv(url2, "data/secondary_data/lsoa_data", "lsoa_data")




def convert_xlsx_to_csvs(xlsx_path, output_dir):
    # Load the XLSX file
    xlsx = pd.ExcelFile(xlsx_path)

    # Check if the output directory exists, if not create it
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    # Iterate through each sheet in the XLSX file
    for sheet_name in xlsx.sheet_names:
        # Read the sheet into a DataFrame
        df = xlsx.parse(sheet_name)

        # Define the CSV file path
        csv_file_path = os.path.join(output_dir, f"{sheet_name}.csv")

        # Save the DataFrame to CSV
        df.to_csv(csv_file_path, index=False)
        print(f"Saved {sheet_name} to {csv_file_path}")

# Usage





def download_and_unzip(url, output_dir):
    """
    Downloads a ZIP file from a given URL and extracts its contents to a specified directory.

    Args:
    url (str): The URL of the ZIP file.
    output_dir (str): Directory to extract the contents of the ZIP file. Defaults to the current directory.

    Returns:
    None
    """
    
    
    os.makedirs(output_dir, exist_ok=True)
    # Get the filename from the URL
    filename = url.split('/')[-1]

    # Download the file
    response = requests.get(url)
    if response.status_code == 200:
        zip_path = os.path.join(output_dir, filename)
        with open(zip_path, 'wb') as file:
            file.write(response.content)
        
        # Unzip the file
        with zipfile.ZipFile(zip_path, 'r') as zip_ref:
            zip_ref.extractall(output_dir)
        
        print(f"File downloaded and extracted in: {output_dir}")
    else:
        print("Failed to download the file")

# Usage example:


#download and save csv
def download_and_save_csv(url, output_dir, output_filename):
    """
    Downloads a CSV file from a given URL and saves it to a specified directory.

    Args:
    url (str): The URL of the CSV file.
    output_dir (str): Directory to save the CSV file.
    output_filename (str): Name of the output CSV file.

    Returns:
    None
    """
    os.makedirs(output_dir, exist_ok=True)
    csv_path = os.path.join(output_dir, output_filename + ".csv")
    response = requests.get(url)
    if response.status_code == 200:
        with open(csv_path, 'wb') as file:
            file.write(response.content)
        print(f"CSV file saved in: {csv_path}")
    else:
        print("Failed to download the CSV file")
        
        


#download json
def download_and_save_json(url, output_dir, output_filename):
    """
    Downloads a JSON file from a given URL and saves it to a specified directory.

    Args:
    url (str): The URL of the JSON file.
    output_dir (str): Directory to save the JSON file.
    output_filename (str): Name of the output JSON file.

    Returns:
    None
    """
    os.makedirs(output_dir, exist_ok=True)
    json_path = os.path.join(output_dir, output_filename + ".json")
    response = requests.get(url)
    if response.status_code == 200:
        with open(json_path, 'wb') as file:
            file.write(response.content)
        print(f"JSON file saved in: {json_path}")
    else:
        print("Failed to download the JSON file")
        
        
#download xlsx and save
def download_xlsx(url, output_dir):
    """
    Downloads an Excel file from a given URL and saves it to a specified directory.

    Args:
    url (str): The URL of the Excel file.
    output_dir (str): Directory to save the Excel file.

    Returns:
    None
    """
    os.makedirs(output_dir, exist_ok=True)
    filename = url.split('/')[-1]
    xlsx_path = os.path.join(output_dir, filename)
    response = requests.get(url)
    if response.status_code == 200:
        with open(xlsx_path, 'wb') as file:
            file.write(response.content)
        print(f"Excel file saved in: {xlsx_path}")
    else:
        print("Failed to download the Excel file")
        
        








url ="https://policeuk-data.s3.amazonaws.com/download/bc01a9eeaca07ca2a833387849b7cab7e2ee06fa.zip"
# url = "https://policeuk-data.s3.amazonaws.com/download/d14653c3a332b4238b9a419afe4a66d8bee6541e.zip"
#download_and_unzip(url,"data/primary_data")




xlsx_path = 'https://data.london.gov.uk/download/mopac-surveys/c3db2a0c-70f5-4b73-916b-2b0fcd9decc0/PAS_T%26Cdashboard_to%20Q3%2023-24.xlsx'
output_dir = 'data/secondary_data/pas_data'
download_xlsx(xlsx_path, output_dir)






uof_links = [
    'https://data.london.gov.uk/download/use-of-force/3b237b91-350d-4b65-a96a-a4de78843eac/MPS%20Use%20of%20Force%20-%20FY24-25.xlsx',
    'https://data.london.gov.uk/download/use-of-force/eb865cae-d67f-492f-9744-9a0d52a0763f/MPS%20Use%20of%20Force%20-%20FY23-24.xlsx',
    'https://data.london.gov.uk/download/use-of-force/606fc688-fc22-44c4-bc95-ca6a53891275/MPS%20Use%20of%20Force%20-%20FY22-23.xlsx',
    'https://data.london.gov.uk/download/use-of-force/ee2453af-1f57-4a4d-909b-c7fe2810ae60/MPS%20Use%20of%20Force%20-%20FY21-22.xlsx',
    'https://data.london.gov.uk/download/use-of-force/9d266ef1-7376-4eec-bb0d-dfbd2b1a591e/MPS%20Use%20of%20Force%20-%20FY20-21.xlsx',
    'https://data.london.gov.uk/download/use-of-force/2aa0d839-add7-46c1-a168-e62d33323228/MPS%20Use%20of%20Force%20-%20FY19-20.xlsx',
    'https://data.london.gov.uk/download/use-of-force/727e768a-a8fe-4c06-bfa3-ac61930bfa78/MPS%20Use%20of%20Force%20-%20FY18-19.xlsx',
    'https://data.london.gov.uk/download/use-of-force/cba04655-0562-4631-ad14-0f3c9f244bbd/MPS%20Use%20of%20Force%20-%20FY17-18.xlsx'
    
]


#reformat file names to change %20 to spaces on file names
def reformat_file_name(link):
    return link.split('/')[-1].replace('%20', ' ')


for link in uof_links:
    
    
    download_xlsx(link, 'data/secondary_data/use_of_force')
    
    
    
for file in os.listdir('data/secondary_data/use_of_force'):
    print(file)
    os.rename(f'data/secondary_data/use_of_force/{file}', f'data/secondary_data/use_of_force/{reformat_file_name(file)}')
    






# URL of the Excel file
url = "https://data.london.gov.uk/download/earnings-place-residence-borough/1686ef1c-b169-442d-8877-e7e49788f668/earnings-residence-borough.xlsx"
url2  = 'https://data.london.gov.uk/download/lsoa-atlas/b8e01c3a-f5e3-4417-82b3-02ad271e6ee8/lsoa-data.xls'

# Call the function with the specified parameters
download_and_convert_excel_to_csv(url, "data/secondary_data/income_by_region", "earnings_residence_borough")
download_and_convert_excel_to_csv(url2, "data/secondary_data/lsoa_data", "lsoa_data")



download_and_unzip("https://data.london.gov.uk/download/statistical-gis-boundary-files-london/9ba8c833-6370-4b11-abdc-314aa020d5e0/statistical-gis-boundaries-london.zip",'data/secondary_data/map')


#download and save csv
def download_and_save_csv(url, output_dir, output_filename):
    """
    Downloads a CSV file from a given URL and saves it to a specified directory.

    Args:
    url (str): The URL of the CSV file.
    output_dir (str): Directory to save the CSV file.
    output_filename (str): Name of the output CSV file.

    Returns:
    None
    """
    os.makedirs(output_dir, exist_ok=True)
    csv_path = os.path.join(output_dir, output_filename + ".csv")
    response = requests.get(url)
    if response.status_code == 200:
        with open(csv_path, 'wb') as file:
            file.write(response.content)
        print(f"CSV file saved in: {csv_path}")
    else:
        print("Failed to download the CSV file")
        
        
download_and_save_csv('https://data.london.gov.uk/download/benefits-analysis/fd8e06be-6546-4c4e-ab0e-f265ea161d94/People_UC_Borough.csv','data/secondary_data/benefits','People_UC_Borough')






download_and_save_csv('https://data.london.gov.uk/download/benefits-analysis/fd8e06be-6546-4c4e-ab0e-f265ea161d94/People_UC_Borough.csv','data/secondary_data/benefits','People_UC_Borough')




download_and_save_json('https://martinjc.github.io/UK-GeoJSON/json/eng/topo_lad.json', 'data/secondary_data/geojson', 'topo_lad')



