import json
from pathlib import Path

import pytest

from weather_etl.transform import to_rows


@pytest.fixture
def forecast_medellin():
    with open(
        Path(__file__).parent / "fixtures" / "forecast_medellin.json"
    ) as f:
        return json.load(f)


def test_get_city_data_to_rows(forecast_medellin):
    """
    Test that the to_rows function correctly transforms the forecast data for
    a given city.

    Args:
        forecast_medellin (_type_): _description_

    Returns:
        None

    Asserts:
        The first row of the transformed data matches the expected dictionary
        for Medellin.
    """
    city = "Medellin"
    rows = to_rows(city, forecast_medellin)
    assert rows[0] == {
        "city": "Medellin",
        "date": "2026-11-13",
        "temperature_2m_max": 28.7,
        "temperature_2m_min": 17.4,
        "precipitation_sum": 1.3,
    }


@pytest.mark.parametrize(
    "field", ["temperature_2m_max", "temperature_2m_min", "precipitation_sum"]
)
def test_drops_day_with_null_value(forecast_medellin, field):
    """
    Drops a day whose value is null.
    """
    city = "Medellin"
    forecast_medellin["daily"][field][0] = None
    rows = to_rows(city, forecast_medellin)
    assert len(rows) == 6
    assert rows[0] == {
        "city": "Medellin",
        "date": "2026-11-14",
        "temperature_2m_max": 27.7,
        "temperature_2m_min": 17.5,
        "precipitation_sum": 1.0,
    }


def test_day_with_many_decimals(forecast_medellin):
    """
    Tests a day with many decimals.
    """
    city = "Medellin"
    forecast_medellin["daily"]["temperature_2m_max"][1] = 27.6666
    rows = to_rows(city, forecast_medellin)
    assert len(rows) == 7
    assert rows[1] == {
        "city": "Medellin",
        "date": "2026-11-14",
        "temperature_2m_max": 27.7,
        "temperature_2m_min": 17.5,
        "precipitation_sum": 1.0,
    }


def test_day_with_empty_list():
    """
    Returns no rows when the daily lists are empty.
    """
    city = "Medellin"
    payload = {
        "daily": {
            "time": [],
            "temperature_2m_max": [],
            "temperature_2m_min": [],
            "precipitation_sum": [],
        }
    }
    rows = to_rows(city, payload)
    assert rows == []
    assert len(rows) == 0


def test_day_row_count(forecast_medellin):
    """
    Returns the correct number of rows when the daily lists are populated.
    """
    city = "Medellin"
    rows = to_rows(city, forecast_medellin)
    assert len(rows) == len(forecast_medellin["daily"]["time"])
