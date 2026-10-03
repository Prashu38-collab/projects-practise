import requests


def get_coordinates(city):
    geocoding_url = "https://geocoding-api.open-meteo.com/v1/search"

    params = {
        "name": city,
        "count": 1,
        "language": "en",
        "format": "json",
    }

    response = requests.get(geocoding_url, params=params)

    if response.status_code != 200:
        print("Could not connect to the geocoding API.")
        return None

    data = response.json()

    if "results" not in data or len(data["results"]) == 0:
        print("City not found.")
        return None

    location = data["results"][0]

    return {
        "name": location["name"],
        "country": location.get("country", "Unknown"),
        "latitude": location["latitude"],
        "longitude": location["longitude"],
    }


def get_weather(latitude, longitude):
    weather_url = "https://api.open-meteo.com/v1/forecast"

    params = {
        "latitude": latitude,
        "longitude": longitude,
        "current": "temperature_2m,wind_speed_10m",
        "temperature_unit": "fahrenheit",
        "wind_speed_unit": "mph",
    }

    response = requests.get(weather_url, params=params)

    if response.status_code != 200:
        print("Could not get weather data.")
        return None

    data = response.json()

    if "current" not in data:
        print("Weather data not available.")
        return None

    return data["current"]


def main():
    city = input("Enter a city: ").strip()

    if not city:
        print("Please enter a valid city name.")
        return

    location = get_coordinates(city)

    if location is None:
        return

    weather = get_weather(location["latitude"], location["longitude"])

    if weather is None:
        return

    print()
    print(f"Weather for {location['name']}, {location['country']}")
    print(f"Temperature: {weather['temperature_2m']}°F")
    print(f"Wind speed: {weather['wind_speed_10m']} mph")


if __name__ == "__main__":
    main()
