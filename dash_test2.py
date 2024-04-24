import dash
from dash import dcc, html, dash_table
from dash.dependencies import Input, Output
import plotly.graph_objects as go
import pandas as pd
import geopandas as gpd
import json

# Load the data
shapefile_path1 = 'data/secondary_data/map/statistical-gis-boundaries-london/ESRI/LSOA_2011_London_gen_MHW.shp'
shapefile_path2 = 'data/secondary_data/map/statistical-gis-boundaries-london/ESRI/London_Borough_Excluding_MHW.shp'  # New borough shapefile
gdf1 = gpd.read_file(shapefile_path1).to_crs("WGS84")
gdf2 = gpd.read_file(shapefile_path2).to_crs("WGS84")
geojson1 = json.loads(gdf1.to_json())
geojson2 = json.loads(gdf2.to_json())

csv_data_path = 'data/primary_data/2021-03/2021-03-metropolitan-street.csv'
csv_data = pd.read_csv(csv_data_path)

# Initialize the Dash app
app = dash.Dash(__name__)

# App layout
app.layout = html.Div([
    dcc.Dropdown(
        id='shapefile-dropdown',
        options=[
            {'label': 'LSOA Shapefile', 'value': 'gdf1'},
            {'label': 'Borough Shapefile', 'value': 'gdf2'}
        ],
        value='gdf1',
        clearable=False
    ),
    dcc.Dropdown(
        id='crime-type-dropdown',
        options=[{'label': i, 'value': i} for i in csv_data['Crime type'].unique()],
        value=['All Crimes'],
        multi=True,
        clearable=True
    ),
    dcc.Graph(id='crime-map'),
    dash_table.DataTable(
        id='crime-data-table',
        columns=[{"name": i, "id": i} for i in csv_data.columns],
        data=[]
    )
])

# Callback to update the map based on selected shapefile and crime types
@app.callback(
    Output('crime-map', 'figure'),
    [Input('shapefile-dropdown', 'value'),
     Input('crime-type-dropdown', 'value')]
)
def update_map(selected_shapefile, crime_types):
    geojson = geojson1 if selected_shapefile == 'gdf1' else geojson2
    gdf = gdf1 if selected_shapefile == 'gdf1' else gdf2
    
    if not crime_types or 'All Crimes' in crime_types:
        df_filtered = csv_data
    else:
        df_filtered = csv_data[csv_data['Crime type'].isin(crime_types)]
    
    crime_counts = df_filtered['LSOA code'].value_counts().reset_index()
    crime_counts.columns = ['LSOA11CD', 'Crime Count']
    merged_gdf = gdf.merge(crime_counts, on='LSOA11CD', how='left').fillna(0)
    
    fig = go.Figure(go.Choroplethmapbox(
        geojson=geojson,
        locations=merged_gdf.index,
        z=merged_gdf['Crime Count'],
        colorscale="Plasma",
        marker_line_width=0.5
    ))
    fig.update_layout(
        mapbox_style="carto-darkmatter",
        mapbox=dict(center=dict(lat=51.5074, lon=-0.1278), zoom=10),
        height=600
    )
    return fig

if __name__ == '__main__':
    app.run_server(debug=True)
