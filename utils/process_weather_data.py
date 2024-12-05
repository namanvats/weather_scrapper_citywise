import os
import sys

import pandas as pd
import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parent.parent))
from utils.generate_file_name import get_csv_file_name_for_given_date
from utils.data_plotter import plot_graphs_from_processed_data
from utils.logger import setup_logger
import matplotlib.pyplot as plt


logger = setup_logger(__name__, "logs/weather_scrapper.log")


def process_weather_data(file_name):
    csv_path = os.path.join(file_name)
    df = pd.read_csv(csv_path)

    df["Temperature (°F)"] = (df["Temperature (°C)"] * 9 / 5) + 32
    df["Wind Speed (mph)"] = df["Wind Speed (m/s)"] * 2.23694

    # Rank cities by highest temperature for each hour
    highest_temp_data = []
    for hour in df["Time"].unique():
        hour_df = df[df["Time"] == hour].sort_values(
            "Temperature (°C)", ascending=False
        )[["City", "Temperature (°C)"]]
        highest_temp_data.append(
            {
                "Hour": hour,
                "City": hour_df["City"].iloc[0],
                "Temperature (°C)": hour_df["Temperature (°C)"].iloc[0],
            }
        )
    highest_temp_df = pd.DataFrame(highest_temp_data)
    highest_temp_df.to_csv("Data/highest_temp_cities.csv", index=False)

    # Rank cities by lowest humidity for each hour
    lowest_humidity_data = []
    for hour in df["Time"].unique():
        hour_df = df[df["Time"] == hour].sort_values(
            "Relative Humidity (%)", ascending=True
        )[["City", "Relative Humidity (%)"]]
        lowest_humidity_data.append(
            {
                "Hour": hour,
                "City": hour_df["City"].iloc[0],
                "Relative Humidity (%)": hour_df["Relative Humidity (%)"].iloc[0],
            }
        )
    lowest_humidity_df = pd.DataFrame(lowest_humidity_data)
    lowest_humidity_df.to_csv("Data/lowest_humidity_cities.csv", index=False)

    # Filter and save only the required columns
    required_columns = [
        "City",
        "Temperature (°C)",
        "Temperature (°F)",
        "Relative Humidity (%)",
        "Wind Speed (m/s)",
        "Wind Speed (mph)",
        "Time",
    ]
    df[required_columns].to_csv("Data/weather_data.csv", index=False)


def main():
    process_weather_data(get_csv_file_name_for_given_date())
    plot_graphs_from_processed_data()


if __name__ == "__main__":
    main()
