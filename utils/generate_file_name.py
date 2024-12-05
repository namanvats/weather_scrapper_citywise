from datetime import date, datetime


def get_csv_file_name_for_given_date():
    today = date.today().strftime("%Y-%m-%d")
    csv_file = f"weather_data/weather_{today}.csv"
    return csv_file


def get_weather_processed_file():
    weather_processed_csv_file = f"Data/weather_data.csv"
    return weather_processed_csv_file


def get_highest_temperature_cities_file():
    highest_temp_cities_csv_file = f"Data/highest_temp_cities.csv"
    return highest_temp_cities_csv_file


def get_lowest_humidity_cities_file():
    lowest_humidity_cities_csv_file = f"Data/lowest_humidity_cities.csv"
    return lowest_humidity_cities_csv_file
