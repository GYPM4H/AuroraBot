import requests
from bs4 import BeautifulSoup

from datetime import datetime
import pytz

from config import get_config

import warnings

config = get_config()

warnings.filterwarnings("ignore", category=UserWarning, module='bs4')

def get_aurora_prob(latitude, longitude):
    """
    Retrieve the aurora probability for given coordinates.
    
    Args:
        latitude (float): The latitude for which to retrieve the aurora probability.
        longitude (float): The longitude for which to retrieve the aurora probability.
    
    Returns:
        float: The aurora probability.
    """
    url = 'https://services.swpc.noaa.gov/json/ovation_aurora_latest.json'
    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        
        utc_now = datetime.now(pytz.utc)
        closest_data_point = None
        min_distance = float('inf')
        
        for point in data['coordinates']:
            lat, lon, prob = point
            
            lat_distance = abs(lat - latitude)
            lon_distance = abs(lon - longitude)
            total_distance = lat_distance + lon_distance
            
            if total_distance < min_distance:
                min_distance = total_distance
                closest_data_point = {'lat': lat, 'lon': lon, 'prob': prob}
        
        return closest_data_point['prob'] if closest_data_point else None
        
    except requests.RequestException as e:
        print(f"Failed to get data from URL {url}: {e}")
        return None

def get_kp_index():
    """
    Retrieve the KP index from the API.
    
    Returns:
        float: The KP index.
        str: The timestamp of the KP index data.
    """
    url = 'https://services.swpc.noaa.gov/products/noaa-planetary-k-index.json'
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        data = response.json()
        
        # Ensure the data is in the expected format
        if isinstance(data, list) and len(data) > 1 and all(isinstance(row, list) for row in data):
            # Extract keys and the latest data entry
            keys = data[0]
            latest_data_entry = data[-1]
            
            # Create a dictionary from the keys and the latest data entry
            latest_data = dict(zip(keys, latest_data_entry))
            
            # Extract the kp index and timestamp
            kp_index = latest_data.get('Kp')
            timestamp = latest_data.get('time_tag')
            
            return kp_index, timestamp
        else:
            print("Unexpected data format from API.")
            return None, None
        
    except requests.RequestException as e:
        print(f"Failed to get data from URL {url}: {e}")
        return None, None

def get_rx_index():
    """
    Retrieve the RX index data by scraping a webpage.
    
    Returns:
        dict: The RX index data for Tartu.
    """
    COLOR_MAPPING = {
        "#00FF00": "Green",
        "#FFFF00": "Yellow",
        "#FFA500": "Orange",
        "#FF0000": "Red",
        "#800000": "Maroon",
    }

    def get_color_name(hex_color):
        """Return the color name corresponding to the hex code."""
        return COLOR_MAPPING.get(hex_color, 'Unknown')

    def extract_data_from_cells(cells):
        """Extract and structure data from the HTML cells."""
        return {
            'city': cells[0].get_text().strip(),
            'latest_hour_rx': {
                'value': cells[1].get_text().strip(),
                'color': get_color_name(cells[1].get('bgcolor'))
            },
            'next_hour_min_rx': {
                'value': cells[2].get_text().strip(),
                'color': get_color_name(cells[2].get('bgcolor'))
            },
            'next_hour_max_rx': {
                'value': cells[3].get_text().strip(),
                'color': get_color_name(cells[3].get('bgcolor'))
            }
        }

    URL = 'https://aurorasnow.fmi.fi/public_service/magforecast_en.html'
    response = requests.get(URL)
    soup = BeautifulSoup(response.content, features="lxml")
    
    for row in soup.find_all('tr'):
        if 'Tartu' in row.get_text():
            cells = row.find_all('td')
            if len(cells) == 4:
                return extract_data_from_cells(cells)
    
    return None



def get_weather():
    """
    Retrieve the weather data from the API.
    
    Returns:
        tuple: A tuple containing weather data.
    """

    url = "http://api.openweathermap.org/data/2.5/weather?id=588409&appid=" + config['WEATHER_TOKEN']

    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        data = response.json()
        
        cloud_density = data['clouds']['all']
        weather_description = data['weather'][0]['description']
        temperature_kelvin = data['main']['temp']
        humidity = data['main']['humidity']
        
        return cloud_density, weather_description, temperature_kelvin, humidity
        
    except requests.RequestException as e:
        print(f"Failed to get data from URL {url}: {e}")
        return None, None, None, None
