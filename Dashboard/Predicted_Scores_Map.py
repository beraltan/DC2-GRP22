import pandas as pd
import geopandas as gpd
import folium
from folium.features import GeoJson, GeoJsonTooltip
import streamlit as st
from streamlit_folium import folium_static
import json
from shapely.geometry import shape

# Load the datasets
trust_data = pd.read_csv(r'C:\Users\danie\PycharmProjects\DC2\qwe\new_trustALL_TIME.csv')
future_scores = pd.read_csv(r'C:\Users\danie\PycharmProjects\DC2\qwe\futurescore2024.csv')

# Add the missing date column to future_scores
future_scores['Date'] = '2024-03-31'

# Filter data for the specified dates
trust_data['Date'] = pd.to_datetime(trust_data['Date'])
latest_2023 = trust_data[trust_data['Date'] == '2023-12-31']
q1_2024 = future_scores

# Select and rename the columns for merging
latest_2023 = latest_2023[['Borough', 'Average Score']].rename(columns={'Average Score': 'Score_2023'})
q1_2024 = q1_2024[['Borough', 'Average Score']].rename(columns={'Average Score': 'Score_2024'})

# Merge datasets on Borough names
merged_data = pd.merge(latest_2023, q1_2024, on='Borough')

# Calculate the change in scores
merged_data['Change'] = merged_data['Score_2024'] - merged_data['Score_2023']
merged_data['Color'] = merged_data['Change'].apply(lambda x: 'green' if x > 0 else 'red')

# Load the GeoJSON file
with open('london_boroughs.geojson') as f:
    geo_data = json.load(f)

# Extract features from the GeoJSON
features = geo_data['features']

# Create a list of GeoDataFrame rows
gdf_list = []
for feature in features:
    properties = feature['properties']
    geom = shape(feature['geometry'])
    gdf_list.append({'geometry': geom, 'properties': properties})

# Convert the list to a GeoDataFrame
boroughs = gpd.GeoDataFrame(gdf_list)

# Set the CRS to WGS84 (EPSG:4326) if not already set
boroughs = boroughs.set_crs("EPSG:4326")

# Ensure the borough names match exactly
boroughs['name'] = boroughs['properties'].apply(lambda x: x['name'].lower())
merged_data['Borough'] = merged_data['Borough'].str.lower()

# Merge the GeoDataFrame with the merged data
boroughs = boroughs.merge(merged_data, left_on='name', right_on='Borough')

# Function to create the map
def create_map():
    # Initialize the map centered around London
    m = folium.Map(location=[51.509865, -0.118092], zoom_start=10)

    # Iterate through the merged data to create map elements
    for _, row in boroughs.iterrows():
        borough_name = row['Borough']
        map_style = {
            'fillColor': row['Color'],
            'color': 'black',
            'weight': 1,
            'fillOpacity': 0.5,
        }
        tooltip = GeoJsonTooltip(
            fields=['name', 'Score_2023', 'Score_2024', 'Change'],
            aliases=['Borough', 'Score in 2023', 'Score in 2024', 'Change']
        )
        geo_json = GeoJson(
            boroughs[boroughs['name'] == borough_name],
            style_function=lambda x, s=map_style: s,
            tooltip=tooltip
        )
        geo_json.add_to(m)

    return m

# Streamlit Dashboard
st.title("London Borough Trust Scores Dashboard")
year_option = st.selectbox("Select Year", ["2023", "2024"])

map = create_map()
folium_static(map)
