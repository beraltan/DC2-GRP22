import dash
from dash import dcc, html, dash_table
from dash.dependencies import Input, Output
import plotly.graph_objects as go
import pandas as pd
import geopandas as gpd
import json

# Load the data
shapefile_path = 'data/secondary_data/map/statistical-gis-boundaries-london/ESRI/LSOA_2011_London_gen_MHW.shp'
gdf = gpd.read_file(shapefile_path).to_crs("WGS84")
csv_data_path = 'data/primary_data/2021-03/2021-03-metropolitan-street.csv'
csv_data = pd.read_csv(csv_data_path)

# Prepare the geojson
geojson = json.loads(gdf.to_json())

# Initialize the Dash app
app = dash.Dash(__name__)

# App layout
app.layout = html.Div([
    dcc.Dropdown(
        id='crime-type-dropdown',
        options=[{'label': i, 'value': i} for i in csv_data['Crime type'].unique()],
        value=['All Crimes'],  # Default value as a list
        multi=True,  # Allow multiple selections
        clearable=True
    ),
    dcc.Graph(id='crime-map', config={'modeBarButtonsToAdd': ['drawrect', 'drawclosedpath', 'eraseshape']}),
    dash_table.DataTable(
        id='crime-data-table',
        columns=[{"name": i, "id": i} for i in csv_data.columns],
        data=[]
    )
])

# Callback to update the map and the data table based on dropdown selection and lasso selection
@app.callback(
    [Output('crime-map', 'figure'),
     Output('crime-data-table', 'data')],
    [Input('crime-type-dropdown', 'value'),
     Input('crime-map', 'selectedData')]
)
def update_map_and_table(crime_types, selectedData):
    if not crime_types or 'All Crimes' in crime_types:
        df_filtered = csv_data
    else:
        df_filtered = csv_data[csv_data['Crime type'].isin(crime_types)]
    
    # Aggregate data
    crime_counts = df_filtered['LSOA code'].value_counts().reset_index()
    crime_counts.columns = ['LSOA11CD', 'Crime Count']
    merged_gdf = gdf.merge(crime_counts, on='LSOA11CD', how='left').fillna(0)
    
    # Update hover text
    merged_gdf['hover_text'] = 'Borough: ' + merged_gdf['LAD11NM'] + '<br>Crime Count: ' + merged_gdf['Crime Count'].astype(str)
    
    # Create the figure
    fig = go.Figure(go.Choroplethmapbox(geojson=geojson,
                                        locations=merged_gdf.index,
                                        z=merged_gdf['Crime Count'],
                                        colorscale="Plasma",
                                        marker_line_width=0.5,
                                        text=merged_gdf['hover_text'],
                                        zmin=1))  # This ensures zero count areas are not colored
    
    fig.update_layout(mapbox_style="carto-darkmatter",
                      height=600,
                      mapbox=dict(center=dict(lat=51.5074, lon=-0.1278), zoom=10))
    
    # Data table update based on lasso selection
    if selectedData and 'points' in selectedData:
        selected_indices = [point['pointIndex'] for point in selectedData['points']]
        selected_lsoa = merged_gdf.iloc[selected_indices]['LSOA11CD'].tolist()
        table_data = csv_data[csv_data['LSOA code'].isin(selected_lsoa)].to_dict('records')
    else:
        table_data = []

    return fig, table_data

# Run the server
if __name__ == '__main__':
    app.run_server(debug=True)
