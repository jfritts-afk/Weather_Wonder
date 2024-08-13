# Weather Wonder

## Description

Weather Wonder is a Python application designed to fetch, organize, and store weather data for a specified location. This tool leverages several libraries and APIs to provide current, hourly, and daily weather forecasts. The application also includes functionality to manage and archive weather data files. This is to be used in a larger project. This project's code can be found [here](https://github.com/jfritts-afk/Robo_Coffee).
- A detailed technical description of this code can also be found [here](/details.md).

## Functionality

### Configuration

The application starts by loading settings from a `config.yaml` file. This configuration file specifies:
- The types of weather data to be retrieved (current, hourly, daily).
- Measurement units for temperature, wind speed, and precipitation.
- Weather model configurations.

### Location Data Retrieval

The user is prompted to enter a location (e.g., city, state, or ZIP code). The application utilizes the Geopy library to:
- Geocode the input location to obtain latitude and longitude.
- Determine the timezone for the location using the Open-Meteo API.

### Weather Data Fetching

With the location data in hand, the application:
- Sets up a cache for API requests to enhance performance and minimize redundant calls.
- Constructs a query to the Open-Meteo API with parameters based on user configuration.
- Retrieves weather data, including current conditions, hourly forecasts, and daily summaries.

### File Management

The application manages weather data files by:
- Saving the most recent weather data to the `most_recent_fetch` directory in YAML format.
- Moving old data files (those older than 15 seconds) from the `most_recent_fetch` directory to the `old_fetch_data` directory. This ensures that only recent data is kept in the primary directory while archiving older data for historical purposes.

### Output

Upon successful execution, the application:
- Displays a message indicating the location where the current weather data has been saved.
- Ensures that old files are properly archived, maintaining an organized data structure.

## Directory Structure

- **most_recent_fetch/**: Contains the most recent weather data files in YAML format.
- **old_fetch_data/**: Contains archived weather data files that are older than 15 seconds.

This application provides an efficient way to manage and archive weather data, ensuring that users have access to the most recent forecasts while maintaining historical records.

## What's the use?
- This project is to build into a larger platform. That project is [here](https://github.com/jfritts-afk/Robo_Coffee)
, Robo_Coffee.