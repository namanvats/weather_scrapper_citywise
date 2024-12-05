import csv
import json
import os
import sys
import pandas as pd
from datetime import date, datetime

import requests

import constants
from utils.generate_file_name import get_csv_file_name_for_given_date
from utils.logger import setup_logger
from utils.city_geo_mapper import fetch_and_build_city_latitude_longitude_data
from utils.process_weather_data import process_weather_data
from utils.data_plotter import plot_graphs_from_processed_data

logger = setup_logger(__name__, "logs/weather_scrapper.log")


def extract_and_save_data_in_csv(weather_data, city_name):
    """
    Extracts relevant weather data and saves it to a CSV file.

    Args:
        weather_data (dict): The weather data retrieved from the Meteo API
        city_name (str): Name of city

    Returns:
        None: Saves the extracted data to a CSV in weather_data folder
    """
    logger.info("Extracting weather data received from API and saving in CSV")

    latitude = weather_data["latitude"]
    longitude = weather_data["longitude"]
    timezone = weather_data["timezone"]

    csv_file = get_csv_file_name_for_given_date()

    if not os.path.exists(csv_file):
        with open(csv_file, "a", newline="") as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(
                [
                    "City",
                    "Latitude",
                    "Longitude",
                    "Weather Code",
                    "Timezone",
                    "Time",
                    "Relative Humidity (%)",
                    "Temperature (°C)",
                    "Wind Speed (m/s)",
                ]
            )

    with open(csv_file, "a", newline="") as csvfile:
        writer = csv.writer(csvfile)

        for i, temp in enumerate(weather_data["hourly"]["temperature_2m"]):
            time = weather_data["hourly"]["time"][i]
            weather_code = weather_data["hourly"]["weather_code"][i]
            wind_speed = weather_data["hourly"]["wind_speed_10m"][i]
            humidity = weather_data["hourly"]["relative_humidity_2m"][i]
            writer.writerow(
                [
                    city_name,
                    latitude,
                    longitude,
                    weather_code,
                    timezone,
                    time,
                    humidity,
                    temp,
                    wind_speed,
                ]
            )


def fetch_city_weather_data(city_name, latitude, longitude):
    """
    Fetches weather data for a specific city using Open Meteo API

    Args:
        city_name (str): Name of the city.
        latitude (float): Latitude of the city.
        longitude (float): Longitude of the city.
    """
    logger.info("Starting to fetch city weather data using meteo api")

    url = constants.WEATHER_API_URL
    params = constants.WEATHER_API_PARAMS

    params["latitude"] = latitude
    params["longitude"] = longitude

    response = requests.get(url=url, params=params)
    if response.status_code == 200:
        logger.info(f"Weather data fetched successfully for {city_name}")
        logger.info(response.json())
        extract_and_save_data_in_csv(response.json(), city_name)
    else:
        logger.error(
            f"API Error while fetching {city_name} weather data, status code: {
                response.status_code}"
        )


def fetch_weather_data_for_cities(cities=None):
    """
    Function to fetch weather data for a list of cities.
    If no cities are provided, it defaults to constants.CITIES.

    Args:
        cities (list): List of city names to fetch weather data for.
    """
    logger.info("Starting to fetch weather data for cities.")

    if not cities:  # Check if cities is None or an empty list
        city_list = constants.CITIES
        logger.info("No cities provided, using predefined cities.")
    else:
        city_list = fetch_and_build_city_latitude_longitude_data(cities)
        logger.info(f"Fetching data for provided cities: {', '.join(cities)}")

    for city in city_list:
        logger.info(f"Fetching data for city : {city}")
        city_name = city["City"]
        latitude = city["Latitude"]
        longitude = city["Longitude"]
        fetch_city_weather_data(city_name, latitude, longitude)


def main():
    city_list = []
    if len(sys.argv) > 1:
        city_list = sys.argv[1:]
        logger.info(f"Cities provided: {', '.join(city_list)}")

    fetch_weather_data_for_cities(city_list)
    process_weather_data(get_csv_file_name_for_given_date())
    plot_graphs_from_processed_data()


if __name__ == "__main__":
    main()
