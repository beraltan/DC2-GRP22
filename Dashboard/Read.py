import json

# Load the GeoJSON file
with open('topo_eerGEO (1).json') as f:
    geo_data = json.load(f)

# Print the keys to inspect the structure
print(geo_data.keys())
