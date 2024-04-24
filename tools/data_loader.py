import requests
import os
import zipfile

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
url = "https://policeuk-data.s3.amazonaws.com/download/d14653c3a332b4238b9a419afe4a66d8bee6541e.zip"
download_and_unzip(url, "data")
