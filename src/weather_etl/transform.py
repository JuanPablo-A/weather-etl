def to_rows(city: str, payload: dict) -> list[dict]:
    """Transform the payload into a list of rows.

    Each row is a dictionary containing the city, date, temperature_2m_max,
    temperature_2m_min, and precipitation_sum. Rows containing any null values
    will be removed. Numerical values a​re rounded to 1 decimal place.

    Args:
        city: The name of the city.
        payload: The JSON payload from the weather API.

    Returns:
        A list of dictionaries, each one representing a row of forecast
        data.
    """

    rows = []
    daily = payload["daily"]
    for time, temperature_2m_max, temperature_2m_min, precipitation_sum in zip(
        daily["time"],
        daily["temperature_2m_max"],
        daily["temperature_2m_min"],
        daily["precipitation_sum"],
        strict=True,
    ):
        if (
            temperature_2m_max is None
            or temperature_2m_min is None
            or precipitation_sum is None
        ):
            continue
        row = {
            "city": city,
            "date": time,
            "temperature_2m_max": round(temperature_2m_max, 1),
            "temperature_2m_min": round(temperature_2m_min, 1),
            "precipitation_sum": round(precipitation_sum, 1),
        }
        rows.append(row)
    return rows
