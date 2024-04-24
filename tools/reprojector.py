from pyproj import Transformer
import pandas as pd

# Load your original data (this step is required if you run this as a standalone script)
# data = pd.read_csv('your_original_file.csv')

# Create a transformer object for WGS 84 to British National Grid conversion
transformer = Transformer.from_crs("epsg:4326", "epsg:27700", always_xy=True)

# Function to reproject coordinates from WGS 84 to British National Grid using Transformer
def reproject(lon, lat, transformer):
    x, y = transformer.transform(lon, lat)
    return x, y

# Apply the transformation to the dataset
data['BNG_easting'], data['BNG_northing'] = zip(*data.apply(lambda row: reproject(row['Longitude'], row['Latitude'], transformer), axis=1))

# Path to save the new CSV
output_csv_path = '/mnt/data/reprojected_crime_data.csv'

# Save the transformed data to a new CSV
data.to_csv(output_csv_path, index=False)

output_csv_path