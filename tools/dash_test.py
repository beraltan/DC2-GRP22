import dash
from dash import dcc, html, Input, Output
import plotly.express as px
import pandas as pd
import requests

# Initialize the Dash app
app = dash.Dash(__name__)

# Define the layout of the app
app.layout = html.Div([
    html.H1("Interactive Crime Map"),
    dcc.Graph(id='crime-map'),
    html.P("Draw a rectangle on the map to select an area."),
    html.Button('Fetch Crimes', id='fetch-crimes', n_clicks=0),
    dcc.Loading(
        id="loading-1",
        type="default",
        children=html.Div(id="loading-output-1")
    )
])

@app.callback(
    Output('crime-map', 'figure'),
    Input('fetch-crimes', 'n_clicks'),
    prevent_initial_call=True
)
def update_map(n_clicks):
    if n_clicks > 0:
        # Coordinates for the center of London as an example
        lat, lon = 51.509865, -0.118092
        url = "https://data.police.uk/api/crimes-street/all-crime"
        params = {'lat': lat, 'lng': lon}
        response = requests.get(url, params=params)
        data = response.json()
        
        df = pd.DataFrame(data)
        if not df.empty:
            df['latitude'] = df['location'].apply(lambda x: x['latitude'])
            df['longitude'] = df['location'].apply(lambda x: x['longitude'])
            fig = px.scatter_geo(df,
                                 lat='latitude',
                                 lon='longitude',
                                 hover_name='category',
                                 scope='europe',
                                 title='Crimes in Selected Area')
            return fig
        else:
            return px.scatter_geo()
    return px.scatter_geo()

# Run the app
if __name__ == '__main__':
    app.run_server(debug=True)
