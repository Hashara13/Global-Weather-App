import requests
from datetime import datetime, timedelta
import math

BASE_URL = "http://api.openweathermap.org/data/2.5/weather"

class WeatherData:
    def __init__(self, city, temperature, humidity, pressure, wind_speed, wind_direction, description, icon):
        self.city = city
        self.temperature = temperature
        self.humidity = humidity
        self.pressure = pressure
        self.wind_speed = wind_speed
        self.wind_direction = wind_direction
        self.description = description
        self.icon = icon
        self.timestamp = datetime.now()

    def to_dict(self):
        return {
            "city": self.city,
            "temperature": self.temperature,
            "humidity": self.humidity,
            "pressure": self.pressure,
            "wind_speed": self.wind_speed,
            "wind_direction": self.wind_direction,
            "description": self.description,
            "icon": self.icon,
            "timestamp": self.timestamp.isoformat()
        }

def kelvin_to_celsius(kelvin):
    return kelvin - 273.15

def kelvin_to_fahrenheit(kelvin):
    return (kelvin - 273.15) * 9/5 + 32

def meters_per_second_to_km_per_hour(speed):
    return speed * 3.6

def meters_per_second_to_miles_per_hour(speed):
    return speed * 2.23694

def degrees_to_cardinal(degrees):
    directions = ["N", "NNE", "NE", "ENE", "E", "ESE", "SE", "SSE", "S", "SSW", "SW", "WSW", "W", "WNW", "NW", "NNW"]
    index = round(degrees / (360 / len(directions))) % len(directions)
    return directions[index]

def fetch_weather_data(city):
    params = {
        "q": city,
        "appid": API_KEY,
        "units": "metric"
    }
    response = requests.get(BASE_URL, params=params)
    if response.status_code == 200:
        data = response.json()
        return WeatherData(
            city=data["name"],
            temperature=data["main"]["temp"],
            humidity=data["main"]["humidity"],
            pressure=data["main"]["pressure"],
            wind_speed=data["wind"]["speed"],
            wind_direction=data["wind"]["deg"],
            description=data["weather"][0]["description"],
            icon=data["weather"][0]["icon"]
        )
    else:
        raise Exception(f"Error fetching weather data: {response.status_code}")

def calculate_heat_index(temperature, humidity):
    if temperature < 27:
        return temperature
    
    c1, c2, c3, c4, c5, c6, c7, c8, c9 = -42.379, 2.04901523, 10.14333127, -0.22475541, -6.83783e-3, -5.481717e-2, 1.22874e-3, 8.5282e-4, -1.99e-6
    heat_index = c1 + c2*temperature + c3*humidity + c4*temperature*humidity + c5*temperature**2 + c6*humidity**2 + c7*temperature**2*humidity + c8*temperature*humidity**2 + c9*temperature**2*humidity**2
    return heat_index

def calculate_wind_chill(temperature, wind_speed):
    if temperature > 10 or wind_speed < 4.8:
        return temperature
    
    wind_chill = 13.12 + 0.6215*temperature - 11.37*(wind_speed**0.16) + 0.3965*temperature*(wind_speed**0.16)
    return wind_chill

def calculate_dew_point(temperature, humidity):
    a = 17.27
    b = 237.7
    alpha = ((a * temperature) / (b + temperature)) + math.log(humidity/100.0)
    dew_point = (b * alpha) / (a - alpha)
    return dew_point

def calculate_visibility(visibility_meters):
    km = visibility_meters / 1000
    miles = km * 0.621371
    return f"{km:.1f} km ({miles:.1f} miles)"

def get_moon_phase(date):
    lunar_cycle = 29.53
    known_new_moon = datetime(2000, 1, 6, 18, 14)
    days_since_known = (date - known_new_moon).days
    phase = (days_since_known % lunar_cycle) / lunar_cycle

    if phase < 0.03 or phase > 0.97:
        return "New Moon"
    elif phase < 0.22:
        return "Waxing Crescent"
    elif phase < 0.28:
        return "First Quarter"
    elif phase < 0.47:
        return "Waxing Gibbous"
    elif phase < 0.53:
        return "Full Moon"
    elif phase < 0.72:
        return "Waning Gibbous"
    elif phase < 0.78:
        return "Last Quarter"
    else:
        return "Waning Crescent"

def calculate_uv_index(latitude, longitude, date):
    solar_noon = datetime(date.year, date.month, date.day, 12, 0)
    time_diff = abs((date - solar_noon).total_seconds() / 3600)
    max_uv = 10 * math.cos(math.radians(latitude))
    uv_index = max_uv * math.cos(math.pi * time_diff / 12)
    return max(0, min(11, round(uv_index)))

def get_air_quality_description(aqi):
    if aqi <= 50:
        return "Good"
    elif aqi <= 100:
        return "Moderate"
    elif aqi <= 150:
        return "Unhealthy for Sensitive Groups"
    elif aqi <= 200:
        return "Unhealthy"
    elif aqi <= 300:
        return "Very Unhealthy"
    else:
        return "Hazardous"

def calculate_feels_like(temperature, humidity, wind_speed):
    heat_index = calculate_heat_index(temperature, humidity)
    wind_chill = calculate_wind_chill(temperature, wind_speed)
    
    if temperature > 27:
        return heat_index
    elif temperature < 10:
        return wind_chill
    else:
        return temperature

def get_weather_warning(temperature, wind_speed, humidity):
    warnings = []
    
    if temperature > 35:
        warnings.append("Extreme heat warning")
    elif temperature < -10:
        warnings.append("Extreme cold warning")
    
    if wind_speed > 20:
        warnings.append("High wind warning")
    
    if humidity > 90:
        warnings.append("High humidity warning")
    
    return warnings if warnings else None

def format_sunrise_sunset(sunrise_timestamp, sunset_timestamp):
    sunrise = datetime.fromtimestamp(sunrise_timestamp)
    sunset = datetime.fromtimestamp(sunset_timestamp)
    day_length = sunset - sunrise
    return {
        "sunrise": sunrise.strftime("%I:%M %p"),
        "sunset": sunset.strftime("%I:%M %p"),
        "day_length": str(day_length).split(".")[0]
    }

def get_weather_icon_url(icon_code):
    return f"http://openweathermap.org/img/wn/{icon_code}@2x.png"

def calculate_precipitation_probability(clouds, humidity):
    return min(100, (clouds + humidity) / 2)

def get_weather_forecast(city, days=5):
    url = f"http://api.openweathermap.org/data/2.5/forecast?q={city}&appid={API_KEY}&units=metric"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        forecast = []
        for item in data['list'][:days*8:8]:
            forecast.append({
                "date": datetime.fromtimestamp(item['dt']).strftime("%Y-%m-%d"),
                "temperature": item['main']['temp'],
                "description": item['weather'][0]['description'],
                "icon": item['weather'][0]['icon']
            })
        return forecast
    else:
        raise Exception(f"Error fetching forecast data: {response.status_code}")

def get_pollution_data(lat, lon):
    url = f"http://api.openweathermap.org/data/2.5/air_pollution?lat={lat}&lon={lon}&appid={API_KEY}"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        return {
            "aqi": data['list'][0]['main']['aqi'],
            "co": data['list'][0]['components']['co'],
            "no": data['list'][0]['components']['no'],
            "no2": data['list'][0]['components']['no2'],
            "o3": data['list'][0]['components']['o3'],
            "so2": data['list'][0]['components']['so2'],
            "pm2_5": data['list'][0]['components']['pm2_5'],
            "pm10": data['list'][0]['components']['pm10'],
            "nh3": data['list'][0]['components']['nh3']
        }
    else:
        raise Exception(f"Error fetching pollution data: {response.status_code}")

class WeatherStation:
    def __init__(self, city):
        self.city = city
        self.data = None
        self.last_update = None

    def update(self):
        self.data = fetch_weather_data(self.city)
        self.last_update = datetime.now()

    def get_current_weather(self):
        if not self.data or (datetime.now() - self.last_update) > timedelta(minutes=10):
            self.update()
        return self.data

    def get_formatted_weather(self):
        weather = self.get_current_weather()
        return {
            "city": weather.city,
            "temperature_c": f"{weather.temperature:.1f}°C",
            "temperature_f": f"{kelvin_to_fahrenheit(weather.temperature + 273.15):.1f}°F",
            "humidity": f"{weather.humidity}%",
            "pressure": f"{weather.pressure} hPa",
            "wind_speed": f"{weather.wind_speed:.1f} m/s ({meters_per_second_to_km_per_hour(weather.wind_speed):.1f} km/h)",
            "wind_direction": f"{weather.wind_direction}° ({degrees_to_cardinal(weather.wind_direction)})",
            "description": weather.description.capitalize(),
            "icon_url": get_weather_icon_url(weather.icon),
            "feels_like": f"{calculate_feels_like(weather.temperature, weather.humidity, weather.wind_speed):.1f}°C",
            "dew_point": f"{calculate_dew_point(weather.temperature, weather.humidity):.1f}°C",
            "uv_index": calculate_uv_index(0, 0, datetime.now()),
            "warnings": get_weather_warning(weather.temperature, weather.wind_speed, weather.humidity)
        }

def main():
    city = "London"
    station = WeatherStation(city)
    weather = station.get_formatted_weather()
    print(f"Current weather in {weather['city']}:")
    print(f"Temperature: {weather['temperature_c']} ({weather['temperature_f']})")
    print(f"Humidity: {weather['humidity']}")
    print(f"Pressure: {weather['pressure']}")
    print(f"Wind: {weather['wind_speed']} {weather['wind_direction']}")
    print(f"Description: {weather['description']}")
    print(f"Feels like: {weather['feels_like']}")
    print(f"Dew point: {weather['dew_point']}")
    print(f"UV Index: {weather['uv_index']}")
    if weather['warnings']:
        print("Warnings:", ", ".join(weather['warnings']))

if __name__ == "__main__":
    main()