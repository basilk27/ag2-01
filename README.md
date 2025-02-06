# ag2-01

$ python --version
Python 3.10.15

$ pip install ag2

create 3 files 
 - group-chat.py
 - two-agent-chat.py
 - conversable-agent.py

 

 
# OpenWeather API Client

A simple Python client for fetching current weather data using the OpenWeather API.

## Prerequisites

- Python 3.6+
- `requests` library
- OpenWeather API key

## Installation

1. Install the required package:
```bash
pip install requests
```

2. Set up your OpenWeather API key as an environment variable:
```bash
export OPENWEATHER_API_KEY='your_api_key_here'
```

## Usage

```python
from openweather import get_weather

# Get weather for a specific location
weather_data = get_weather("Toronto", "Ontario", "CA")
if weather_data:
    print(f"Weather data: {weather_data}")
```

The `get_weather` function takes three parameters:
- `town`: Name of the town/city
- `province`: Province/state
- `country`: Country code (e.g., 'US', 'CA')

## Getting an API Key

1. Sign up at [OpenWeather](https://openweathermap.org/api)
2. Generate an API key from your account
3. Set the API key as an environment variable named `OPENWEATHER_API_KEY`