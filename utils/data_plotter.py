import os
import sys
from pathlib import Path

import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.ticker import MaxNLocator

sys.path.append(str(Path(__file__).resolve().parent.parent))
from utils.generate_file_name import (
    get_weather_processed_file,
    get_highest_temperature_cities_file,
    get_lowest_humidity_cities_file,
)


def plot_temperature_vs_city(data):
    """
    Plot temperature vs city as a bar chart.
    """

    plt.figure(figsize=(10, 6))
    plt.bar(
        data["City"],
        data["Temperature (°F)"],
        color="skyblue",
        label="Temperature (°F)",
    )
    plt.xlabel("City")
    plt.ylabel("Temperature (°F)")
    plt.title("Temperature (°F) by City")
    plt.xticks(rotation=45, ha="right")
    plt.legend()
    plt.tight_layout()
    plt.savefig("Graphs/temperature_by_city.png")
    plt.show(block=False)


def plot_wind_speed_vs_city(data):
    """
    Plot wind speed vs city as a bar chart.
    """
    plt.figure(figsize=(10, 6))
    plt.bar(
        data["City"], data["Wind Speed (mph)"], color="orange", label="Wind Speed (mph)"
    )
    plt.xlabel("City")
    plt.ylabel("Wind Speed (mph)")
    plt.title("Wind Speed (mph) by City")
    plt.xticks(rotation=45, ha="right")
    plt.legend()
    plt.tight_layout()
    plt.savefig("Graphs/wind_speed_by_city.png")
    plt.show(block=False)


def plot_temperature_vs_wind_speed(data):
    """
    Plot temperature vs wind speed as a scatter plot.
    """
    plt.figure(figsize=(10, 6))
    plt.scatter(
        data["Temperature (°F)"],
        data["Wind Speed (m/s)"],
        color="green",
        label="Data Points",
    )
    plt.xlabel("Temperature (°F)")
    plt.ylabel("Wind Speed (mph)")
    plt.title("Temperature vs. Wind Speed")
    plt.grid(alpha=0.3)
    plt.legend()
    plt.tight_layout()
    plt.savefig("Graphs/temperature_vs_wind_speed.png")
    plt.show(block=False)


def plot_highest_temperature_over_time(data):
    """
    Plot the highest temperature over time as a line chart.
    """
    plt.figure(figsize=(10, 6))
    plt.plot(
        data["Hour"],
        data["Temperature (°F)"],
        marker="o",
        color="red",
        label="Highest Temp (°F)",
    )
    plt.xlabel("Hour")
    plt.ylabel("Temperature (°F)")
    plt.title("Highest Temperature Over Time")
    plt.grid(alpha=0.3)
    plt.legend()
    plt.tight_layout()
    plt.savefig("Graphs/highest_temperature_over_time.png")
    plt.show(block=False)


def plot_lowest_humidity_over_time(data):
    """
    Plot the lowest humidity over time as a line chart.
    """
    plt.figure(figsize=(10, 6))
    plt.plot(
        data["Hour"],
        data["Relative Humidity (%)"],
        marker="o",
        color="blue",
        label="Lowest Humidity (%)",
    )
    plt.xlabel("Hour")
    plt.ylabel("Relative Humidity (%)")
    plt.title("Lowest Humidity Over Time")
    plt.grid(alpha=0.3)
    plt.legend()
    plt.tight_layout()
    plt.savefig("Graphs/lowest_humidity_over_time.png")
    plt.show(block=False)


def plot_city_temperature_vs_time(data, selected_city=None):
    """
    Plot temperature vs time for each city as a line chart.
    If selected_city is provided, only plot data for that city.
    """
    plt.figure(figsize=(12, 8))

    if selected_city:
        city_data = data[data["City"] == selected_city]
        plt.plot(
            city_data["Time"],
            city_data["Temperature (°F)"],
            marker="o",
            label=f"{selected_city}",
        )
    else:
        cities = data["City"].unique()
        for city in cities:
            city_data = data[data["City"] == city]
            plt.plot(
                city_data["Time"],
                city_data["Temperature (°F)"],
                marker="o",
                label=city,
            )

    plt.xlabel("Time")
    plt.ylabel("Temperature (°F)")
    plt.title(
        f"City Temperature vs. Time{' - ' + selected_city if selected_city else ''}"
    )
    plt.xticks(rotation=45, ha="right")

    ax = plt.gca()
    ax.xaxis.set_major_locator(MaxNLocator(nbins=10))

    plt.legend(title="City")
    plt.grid(alpha=0.3)
    plt.tight_layout()

    filename = f"Graphs/city_temperature_vs_time_{selected_city if selected_city else 'all'}.png"
    plt.savefig(filename)
    plt.show(block=False)


def plot_graphs_from_processed_data():

    weather_data = pd.read_csv(get_weather_processed_file())
    highest_temp_data = pd.read_csv(get_highest_temperature_cities_file())
    lowest_humidity_data = pd.read_csv(get_lowest_humidity_cities_file())

    plot_temperature_vs_city(weather_data)
    plot_wind_speed_vs_city(weather_data)
    plot_temperature_vs_wind_speed(weather_data)
    plot_highest_temperature_over_time(highest_temp_data)
    plot_lowest_humidity_over_time(lowest_humidity_data)
    plot_city_temperature_vs_time(weather_data)

    # Show all plots at once
    plt.show()  # Comment this line to avoid showing graphs directly
