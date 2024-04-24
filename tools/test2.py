import os
from flask import Flask, render_template, request, send_from_directory
import requests
import pandas as pd
import folium
from datetime import datetime

app = Flask(__name__)

# Ensure static directory exists
if not os.path.exists('static'):
    os.makedirs('static')

def fetch_crime_data(lat, lng, date):
    """Fetch crime data for a specific month and location."""
    url = f"https://data.police.uk/api/crimes-street/all-crime?lat={lat}&lng={lng}&date={date}"
    response = requests.get(url)
    return pd.DataFrame(response.json()) if response.ok else pd.DataFrame()

def generate_date_options():
    current_year = datetime.now().year
    years = list(range(2015, current_year + 1))
    months = [f"{i:02d}" for i in range(1, 13)]
    return years, months

@app.route('/', methods=['GET', 'POST'])
def home():
    years, months = generate_date_options()
    if request.method == 'POST':
        start_year = request.form['start_year']
        start_month = request.form['start_month']
        end_year = request.form['end_year']
        end_month = request.form['end_month']
        start_date = f"{start_year}-{start_month}"
        end_date = f"{end_year}-{end_month}"

        start = datetime.strptime(start_date, "%Y-%m")
        end = datetime.strptime(end_date, "%Y-%m")
        delta = pd.date_range(start, end, freq='MS')

        lat, lng = 51.5074, -0.1278  # London coordinates
        all_data = pd.concat([fetch_crime_data(lat, lng, dt.strftime("%Y-%m")) for dt in delta], ignore_index=True)

        # Create and save the map
        crime_map = folium.Map(location=[lat, lng], zoom_start=12)
        for _, row in all_data.iterrows():
            folium.CircleMarker(
                location=[row['location']['latitude'], row['location']['longitude']],
                radius=5,
                popup=f"{row['category']} on {row['month']}",
                color='blue',
                fill=True,
                fill_color='blue'
            ).add_to(crime_map)
        
        map_path = 'static/map.html'
        crime_map.save(map_path)

        return send_from_directory('static', 'map.html')
    return render_template('form.html', years=years, months=months)

if __name__ == "__main__":
    app.run(debug=True)
