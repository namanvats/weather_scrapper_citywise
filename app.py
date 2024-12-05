from fastapi import FastAPI, HTTPException, Query
from fastapi.responses import FileResponse
from pathlib import Path

app = FastAPI()

BASE_DIR = Path(__file__).resolve().parent
GRAPHS_DIR = BASE_DIR / "Graphs"
DATA_DIR = BASE_DIR / "Data"

# Data CSV Files
CSV_FILES = {
    "weather": DATA_DIR / "weather_data.csv",
    "highest_temp": DATA_DIR / "highest_temp_cities.csv",
    "lowest_humidity": DATA_DIR / "lowest_humidity_cities.csv",
}

# Mapping of graph types to their respective file paths
GRAPH_FILES = {
    "city_temperature_time": GRAPHS_DIR / "city_temperature_vs_time_all.png",
    "highest_temperature_time": GRAPHS_DIR / "highest_temperature_over_time.png",
    "lowest_humidity_time": GRAPHS_DIR / "lowest_humidity_over_time.png",
    "temperature_city": GRAPHS_DIR / "temperature_by_city.png",
    "temperature_wind_speed": GRAPHS_DIR / "temperature_vs_wind_speed.png",
    "wind_speed_city": GRAPHS_DIR / "wind_speed_by_city.png",
}


@app.get("/")
def home():
    """
    Root endpoint with available API details.

    Returns:
        dict: A JSON response with available API endpoints.
    """
    return {
        "weather_data_csv": "/data?type=weather",
        "highest_temp_csv": "/data?type=highest_temp",
        "lowest_humidity_csv": "/data?type=lowest_humidity",
        "temperature_city_graph": "/graphs?type=temperature_city",
        "city_temperature_time_graph": "/graphs?type=city_temperature_time",
        "highest_temperature_time_graph": "/graphs?type=highest_temperature_time",
        "lowest_humidity_time_graph": "/graphs?type=lowest_humidity_time",
        "temperature_wind_speed_graph": "/graphs?type=temperature_wind_speed",
        "wind_speed_city_graph": "/graphs?type=wind_speed_city",
    }


@app.get("/graphs")
def get_graph_file(
    type: str = Query(..., description="Type of graph to fetch"),
    download: bool = Query(
        False, description="Set to True to download the graph instead of viewing"
    ),
):
    """
    Serve the requested graph based on the type.

    Args:
        type (str): The type of graph to fetch.

    Returns:
        FileResponse: The requested graph file.
    """
    if type not in GRAPH_FILES:
        raise HTTPException(
            status_code=400,
            detail=f"Invalid type. Allowed values are: {', '.join(GRAPH_FILES.keys())}.",
        )

    graph_file = GRAPH_FILES[type]
    if not graph_file.exists() or not graph_file.is_file():
        raise HTTPException(
            status_code=404,
            detail=f"{type.replace('_', ' ').capitalize()} graph not found.",
        )
    headers = (
        {"Content-Disposition": f"attachment; filename={type}.png"}
        if download
        else None
    )
    return FileResponse(graph_file, media_type="image/png", headers=headers)


@app.get("/data")
def get_weather_data(
    type: str = Query(
        ...,
        description="Type of data to fetch (weather, highest_temp, lowest_humidity)",
    )
):
    """
    Serve the requested CSV file based on the type.

    Args:
        type (str): The type of CSV data to fetch (weather, highest_temp, lowest_humidity).

    Returns:
        FileResponse: The requested CSV file.
    """
    if type not in CSV_FILES:
        raise HTTPException(
            status_code=400,
            detail=f"Invalid type. Allowed values are: {', '.join(CSV_FILES.keys())}.",
        )

    csv_file = CSV_FILES[type]
    if not csv_file.exists() or not csv_file.is_file():
        raise HTTPException(
            status_code=404, detail=f"{type.capitalize()} data not found."
        )

    return FileResponse(csv_file, media_type="text/csv", filename=f"{type}_data.csv")
