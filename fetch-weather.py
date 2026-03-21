import requests
import json
import os
from datetime import datetime
from dotenv import load_dotenv

# 1. LOAD SECRETS FIRST
# This must happen before any functions are called
load_dotenv()
API_KEY = os.getenv("OPENWEATHER_API_KEY")

BASE_URL = "https://api.openweathermap.org/data/2.5/weather"

def get_weather(city):
    """Fetch current weather data for a given city."""
    if not API_KEY:
        print("Error: API Key missing. Check your .env file!")
        return None

    try:
        params = {
            'q': city,
            'appid': API_KEY, # Using the variable loaded at the top
            'units': 'metric'
        }

        response = requests.get(BASE_URL, params=params)
        response.raise_for_status() 

        data = response.json()

        return {
            'city': data['name'],
            'country': data['sys']['country'],
            'temperature': data['main']['temp'],
            'feels_like': data['main']['feels_like'],
            'humidity': data['main']['humidity'],
            'description': data['weather'][0]['description'],
            'wind_speed': data['wind']['speed'],
            'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        }

    except requests.exceptions.RequestException as e:
        print(f"Error fetching weather for {city}: {e}")
        return None

# ... [Keep your display_weather and save_to_file functions here] ...

def display_weather(weather_data):
    if weather_data is None:
        print("No weather data to display.")
        return

    print("\n" + "="*50)
    print(f"Weather in {weather_data['city']}, {weather_data['country']}")
    print("="*50)
    print(f"Temperature: {weather_data['temperature']}°C")
    print(f"Feels Like: {weather_data['feels_like']}°C")
    print(f"Conditions: {weather_data['description'].title()}")
    print(f"Time: {weather_data['timestamp']}")
    print("="*50 + "\n")

def save_to_file(weather_data, filename='weather_data.json'):
    if weather_data is None: return
    try:
        try:
            with open(filename, 'r') as f:
                all_data = json.load(f)
        except FileNotFoundError:
            all_data = []
        all_data.append(weather_data)
        with open(filename, 'w') as f:
            json.dump(all_data, f, indent=2)
        print(f"✓ Data saved to {filename}")
    except Exception as e:
        print(f"Error saving data: {e}")

def main():
    print("Welcome to Weather Data Analyzer!")
    while True:
        print("\nOptions: 1. Check City | 2. Exit")
        choice = input("Choice: ").strip()
        if choice == '1':
            city = input("Enter city: ").strip()
            if city:
                weather = get_weather(city)
                display_weather(weather)
                if weather and input("Save? (y/n): ").lower() == 'y':
                    save_to_file(weather)
        elif choice == '2':
            break

if __name__ == "__main__":
    main()