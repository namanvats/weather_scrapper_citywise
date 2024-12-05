import requests
import os
import requests
import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parent.parent))
import constants


def fetch_and_build_city_latitude_longitude_data(city_list):
    """
    Fetch latitude and longitude for a list of cities and return a list of dictionaries.
    Picks the first result from the API response for each city.

    Args:
        city_list (list): List of city names.

    Returns:
        list: A list of dictionaries with city, latitude, and longitude.
    """
    api_url = constants.GEO_NINJAS_API_URL
    api_key = os.getenv("NINJAS_API_KEY")  # API key from env variable

    if not api_key:
        print("Error: NINJAS_API_KEY environment variable is not set.")
        return []

    city_data = []

    for city in city_list:
        try:
            url = api_url.format(city)
            response = requests.get(url, headers={"X-Api-Key": api_key})

            if response.status_code == 200:
                data = response.json()
                if data:
                    first_result = data[0]
                    city_info = {
                        "City": city,
                        "Latitude": first_result["latitude"],
                        "Longitude": first_result["longitude"],
                    }
                    city_data.append(city_info)
                    print(f"Fetched data for {city}: {city_info}")
                else:
                    print(f"No data found for city: {city}")
            else:
                print(
                    f"Error fetching data for {city}: {response.status_code} - {response.text}"
                )
        except Exception as e:
            print(f"Exception occurred while fetching data for {city}: {e}")
    return city_data


if __name__ == "__main__":
    city_list = ["London", "Paris", "Berlin"]

    city_lat_lon_data = fetch_and_build_city_latitude_longitude_data(city_list)

    print(city_lat_lon_data)
