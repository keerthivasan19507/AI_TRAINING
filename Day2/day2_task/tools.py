import requests


def get_weather(city):
    """
    Gets current weather information using Open-Meteo.
    """

    coordinates = {
        "chennai": (13.0827, 80.2707),
        "bangalore": (12.9716, 77.5946),
        "mumbai": (19.0760, 72.8777)
    }

    city_key = city.lower()

    if city_key not in coordinates:
        return {
            "error": f"Weather data for {city} is not configured."
        }

    latitude, longitude = coordinates[city_key]

    url = (
        "https://api.open-meteo.com/v1/forecast"
        f"?latitude={latitude}"
        f"&longitude={longitude}"
        "&current=temperature_2m,precipitation,rain,weather_code"
    )

    response = requests.get(url, timeout=10)
    response.raise_for_status()

    data = response.json()

    current = data["current"]

    return {
        "city": city,
        "temperature_celsius": current["temperature_2m"],
        "precipitation_mm": current["precipitation"],
        "rain_mm": current["rain"],
        "weather_code": current["weather_code"]
    }