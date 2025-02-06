import os
import requests
from typing import Optional

def get_weather(town: str, province: str, country: str) -> Optional[dict]:
    """
    Get current weather data for a location using OpenWeather API.
    
    Args:
        town (str): Name of the town/city
        province (str): Province/state
        country (str): Country code (e.g., 'US', 'CA')
    
    Returns:
        Optional[dict]: Weather data if successful, None if failed
    
    Raises:
        ValueError: If API key is not set or invalid location
    """
    api_key = os.getenv('OPENWEATHER_API_KEY')
    if not api_key:
        raise ValueError("OpenWeather API key not found. Set OPENWEATHER_API_KEY environment variable.")

    # Combine location components with commas, no spaces
    location = f"{town},{province},{country}"
    
    # OpenWeather API endpoint
    base_url = "http://api.openweathermap.org/data/2.5/weather"
    
    # Parameters for the API request
    params = {
        'q': location,
        'appid': api_key,
        'units': 'metric'  # Use metric units
    }
    
    try:
        response = requests.get(base_url, params=params)
        response.raise_for_status()  # Raise exception for bad status codes
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error fetching weather data: {e}")
        return None

# Example usage:
if __name__ == "__main__":
    # Example: Get weather for Toronto, Ontario, Canada
    weather_data = get_weather("Toronto", "Ontario", "CA")
    if weather_data:
        print(f"Weather data: {weather_data}")