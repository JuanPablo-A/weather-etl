import weather_etl


def test_smoke():
    assert weather_etl.__version__ is not None
