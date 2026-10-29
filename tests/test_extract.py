import pytest
import requests

from weather_etl import extract


@pytest.fixture
def sample_cities():
    return {
        "Medellin": {"latitude": 6.245, "longitude": -75.5715},
    }


@pytest.fixture
def fake_forecast():
    return {
        "latitude": 6.2214413,
        "longitude": -75.55185,
        "timezone": "America/Bogota",
        "daily_units": {
            "time": "iso8601",
            "temperature_2m_max": "°C",
            "temperature_2m_min": "°C",
            "precipitation_sum": "mm",
        },
        "daily": {
            "time": ["2026-10-22", "2026-10-23"],
            "temperature_2m_max": [28.5, 28.4],
            "temperature_2m_min": [16.5, 17.4],
            "precipitation_sum": [9.0, 15.2],
        },
    }


def test_get_city_data_returns_forecast_per_city(
    monkeypatch, sample_cities, fake_forecast
):
    def fake_fetch_forecast(latitude, longitude):
        return fake_forecast

    monkeypatch.setattr(extract, "fetch_forecast", fake_fetch_forecast)
    result = extract.get_city_data(sample_cities)
    assert "Medellin" in result[0]["city"]
    assert result[0]["forecast"]["daily"] == fake_forecast["daily"]


def test_get_city_data_path_error(monkeypatch, sample_cities, caplog):
    def fake_fetch_forecast(latitude, longitude):
        raise requests.exceptions.RequestException("API error")

    monkeypatch.setattr(extract, "fetch_forecast", fake_fetch_forecast)
    result = extract.get_city_data(sample_cities)
    assert len(result) == 0
    assert "HTTP error occurred" in caplog.text
