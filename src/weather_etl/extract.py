import logging

import requests

CITIES = {
    "Medellin": {"latitude": 6.245, "longitude": -75.5715},
    "La Ceja": {"latitude": 6.0313, "longitude": -75.4333},
    "Bogota": {"latitude": 4.6097, "longitude": -74.0817},
}


def fetch_forecast(
    latitude,
    longitude,
    timezone="auto",
    daily="temperature_2m_max,temperature_2m_min,precipitation_sum",
) -> dict:
    payload = {
        "latitude": latitude,
        "longitude": longitude,
        "timezone": timezone,
        "daily": daily,
    }
    url = "https://api.open-meteo.com/v1/forecast"
    response = requests.get(url, params=payload, timeout=10)
    response.raise_for_status()

    return response.json()


def get_city_data(cities: dict) -> list[dict]:
    data_list = []

    for key, coords in cities.items():
        try:
            data_list.append(
                {
                    "city": key,
                    "forecast": fetch_forecast(
                        coords["latitude"], coords["longitude"]
                    ),
                }
            )
        except requests.exceptions.RequestException as e:
            logging.error("%s HTTP error occurred %s", key, e)
    return data_list


if __name__ == "__main__":
    print(get_city_data(CITIES))
