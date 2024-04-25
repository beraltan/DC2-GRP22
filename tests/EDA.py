import dash
from dash import dcc, html, Input, Output
import plotly.express as px
import pandas as pd

# Load your data
file_path = './data/primary_data/concatenated_csvs/metropolitan-street.csv'
data = pd.read_csv(file_path)

# Convert 'Month' to datetime and group data to count occurrences
data['Month'] = pd.to_datetime(data['Month'], errors='coerce')
grouped_data = data.groupby(['Crime type', 'Month']).size().reset_index(name='Occurrences')

# Create a Dash application
app = dash.Dash(__name__)

# Layout of the application
app.layout = html.Div([
    dcc.Checklist(
        id='crime-type-selector',
        options=[{'label': i, 'value': i} for i in grouped_data['Crime type'].unique()],
        value=[grouped_data['Crime type'].unique()[0]],  # Default selects the first crime type
        labelStyle={'display': 'block'}
    ),
    dcc.Graph(id='crime-graph')
])

# Callback to update the graph based on selected crime types
@app.callback(
    Output('crime-graph', 'figure'),
    [Input('crime-type-selector', 'value')]
)
def update_graph(selected_crimes):
    filtered_data = grouped_data[grouped_data['Crime type'].isin(selected_crimes)]
    fig = px.line(filtered_data, x='Month', y='Occurrences', color='Crime type',
                  labels={'Month': 'Month of the Year', 'Occurrences': 'Number of Occurrences'},
                  title='Crime Occurrences by Month for Selected Crime Types')
    return fig

# Run the Dash app
if __name__ == '__main__':
    app.run_server(debug=True)