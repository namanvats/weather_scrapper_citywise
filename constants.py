CITIES = [
    {"City": "New York", "Latitude": 40.7128, "Longitude": -74.0060},
    {"City": "Tokyo", "Latitude": 35.6895, "Longitude": 139.6917},
    {"City": "London", "Latitude": 51.5074, "Longitude": -0.1278},
    {"City": "Paris", "Latitude": 48.8566, "Longitude": 2.3522},
    {"City": "Berlin", "Latitude": 52.5200, "Longitude": 13.4050},
    {"City": "Sydney", "Latitude": -33.8688, "Longitude": 151.2093},
    {"City": "Mumbai", "Latitude": 19.0760, "Longitude": 72.8777},
    {"City": "Cape Town", "Latitude": -33.9249, "Longitude": 18.4241},
    {"City": "Moscow", "Latitude": 55.7558, "Longitude": 37.6173},
    {"City": "Rio de Janeiro", "Latitude": -22.9068, "Longitude": -43.1729},
]

WEATHER_API_URL = "https://api.open-meteo.com/v1/forecast"

WEATHER_API_PARAMS = {
    "latitude": "${replace_city_latitude}",
    "longitude": "${replace_city_longitude}",
    "hourly": [
        "temperature_2m",
        "relative_humidity_2m",
        "weather_code",
        "wind_speed_10m",
    ],
    "timezone": "GMT",
    "wind_speed_unit": "ms",
    "past_days": 3,
}

GEO_NINJAS_API_URL = "https://api.api-ninjas.com/v1/geocoding?city={}"
