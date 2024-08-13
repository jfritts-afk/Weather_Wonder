import yaml
import requests
import requests_cache
import os
import shutil
from datetime import datetime
from geopy.geocoders import Nominatim

# Load configuration from YAML file
with open('config.yaml', 'r') as file:
    config = yaml.safe_load(file)

# Function to get latitude, longitude, and timezone from a location
def get_location_data(location):
    geolocator = Nominatim(user_agent="weather_app")
    location_obj = geolocator.geocode(location)
    if location_obj:
        timezone_url = f"https://api.open-meteo.com/v1/timezone?latitude={location_obj.latitude}&longitude={location_obj.longitude}"
        timezone_response = requests.get(timezone_url).json()
        return {
            "latitude": location_obj.latitude,
            "longitude": location_obj.longitude,
            "timezone": timezone_response.get("timezone")
        }
    else:
        return None

# Get the user's input for location
user_input = input("Enter the location (city, state or ZIP code) for the weather forecast: ")

# Get the location data (latitude, longitude, timezone)
location_data = get_location_data(user_input)
if not location_data:
    print("Could not find the location. Please try again.")
    exit()

# Setup the Open-Meteo API client with cache
cache_session = requests_cache.CachedSession('.cache', expire_after=3600)

# Set up the parameters for the weather API request
params = {
    "latitude": location_data["latitude"],
    "longitude": location_data["longitude"],
    "timezone": location_data["timezone"],
    "current": config['weather']['current'],
    "hourly": config['weather']['hourly'],
    "daily": config['weather']['daily'],
    "temperature_unit": config['units']['temperature'],
    "wind_speed_unit": config['units']['wind_speed'],
    "precipitation_unit": config['units']['precipitation'],
    "models": config['units']['models']
}

# Get the weather data
response = requests.get("https://api.open-meteo.com/v1/forecast", params=params).json()

# Define directory paths
most_recent_dir = 'most_recent_fetch'
old_fetch_dir = 'old_fetch_data'

# Ensure directories exist
os.makedirs(most_recent_dir, exist_ok=True)
os.makedirs(old_fetch_dir, exist_ok=True)

# Move old files to the old fetch directory
def move_old_files():
    now = datetime.now()
    print(f"Current time: {now}")
    print(f"Files in '{most_recent_dir}': {os.listdir(most_recent_dir)}")
    for file in os.listdir(most_recent_dir):
        file_path = os.path.join(most_recent_dir, file)
        if os.path.isfile(file_path) and file.endswith('.yaml'):
            file_time = datetime.fromtimestamp(os.path.getmtime(file_path))
            print(f"Checking file: {file_path}, last modified: {file_time}")
            if (now - file_time).total_seconds() > 15:  # 15 Seconds old
                try:
                    print(f"Moving file: {file_path} to {old_fetch_dir}")
                    shutil.move(file_path, old_fetch_dir)
                except Exception as e:
                    print(f"Error moving file {file_path}: {e}")
            else:
                print(f"File is not old enough to move: {file_path}")

# Call the function to move old files
move_old_files()

# Generate filename based on current timestamp
timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
filename = f"weather_data_{timestamp}.yaml"
current_file_path = os.path.join(most_recent_dir, filename)

# Save the current data to the most recent directory in YAML format
with open(current_file_path, 'w') as file:
    yaml.dump(response, file, default_flow_style=False)

print(f"Data saved to {current_file_path}")
