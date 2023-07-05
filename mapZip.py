import requests
import pandas as pd
import folium
from geopy.geocoders import Nominatim

# API endpoint URL
url = "https://datasets-server.huggingface.co/rows?dataset=mda%2Fzipcode&config=mda--zipcode&split=train&offset=0&limit=100"

# Send GET request to the API
response = requests.get(url)

# Check if the API request was successful
if response.status_code == 200:
    # Parse the API response as JSON
    api_data = response.json()

    # Extract the column names
    columns = [feature['name'] for feature in api_data['features']]

    # Find the indices of the desired columns
    column_indices = {}
    for i, column in enumerate(columns):
        column_indices[column] = i

    # Extract the data rows
    rows = api_data['rows']

    # Create a dictionary to store the zip code data
    zip_code_data = {}

    # Initialize the geocoder
    geolocator = Nominatim(user_agent="my_geocoder")

    # Iterate over the rows and extract the zip code, poverty level, and medium household income
    for row in rows[:25]:
        row_data = row['row']
        if 'zip_code' in row_data and 'population_below_poverty_level' in row_data and 'median_household_income' in row_data:
            zip_code = row_data['zip_code']
            poverty_level = float(row_data['population_below_poverty_level'])
            median_income = float(row_data['median_household_income'])
            location = geolocator.geocode(zip_code)
            if location is not None:
                latitude = location.latitude
                longitude = location.longitude
                zip_code_data[zip_code] = {
                    'Poverty Level': poverty_level,
                    'Median Income': median_income,
                    'Latitude': latitude,
                    'Longitude': longitude
                }

    # Create a map centered around the first zip code
    initial_zip_code = list(zip_code_data.keys())[0]
    initial_location = zip_code_data[initial_zip_code]
    map_center = [initial_location['Latitude'], initial_location['Longitude']]
    map_zoom = 10
    map_obj = folium.Map(location=map_center, zoom_start=map_zoom)

    # Add markers or radius circles for each zip code
    for zip_code, location_data in zip_code_data.items():
        poverty_level = location_data['Poverty Level']
        median_income = location_data['Median Income']
        latitude = location_data['Latitude']
        longitude = location_data['Longitude']

        # Create a circle marker with a popup label showing the poverty level and median income
        folium.CircleMarker(
            location=[latitude, longitude],
            radius=poverty_level * 0.5,
            color='red',
            fill=True,
            fill_color='red',
            fill_opacity=0.5,
            popup=f"Zip Code: {zip_code}<br>Poverty Level: {poverty_level}%<br>Median Income: ${median_income}"
        ).add_to(map_obj)

    # Display the map
    map_obj.save('zipcode_map.html')  # Save the map as an HTML file
    print("Map saved as 'zipcode_map.html'.")
else:
    print("Invalid response from the API.")
