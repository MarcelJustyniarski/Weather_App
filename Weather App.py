import requests
from datetime import datetime, timedelta

def get_weather_data(city, api_key):
    url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric&lang=pl"
    response = requests.get(url)
    
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Błąd: {response.status_code}, {response.text}")
        return None

def get_forecast_data(city, api_key):
    url = f"https://api.openweathermap.org/data/2.5/forecast?q={city}&appid={api_key}&units=metric&lang=pl"
    response = requests.get(url)
    
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Błąd: {response.status_code}, {response.text}")
        return None

def format_visibility(visibility):
    if visibility is None:
        return "Brak danych na temat widoczności."
    
    visibility_km = round(visibility / 1000)
    if visibility_km <= 1:
        return f"Widoczność: {visibility_km} km. Bardzo słaba - możliwa mgła, deszcz lub smog."
    elif 1 < visibility_km <= 5:
        return f"Widoczność: {visibility_km} km. Słaba - lekka mgła lub opady."
    elif 6 <= visibility_km <= 9:
        return f"Widoczność: {visibility_km} km. Dobra - lekkie zamglenie."
    else:
        return f"Widoczność: {visibility_km} km. Bardzo dobra - czyste powietrze."

def format_pressure(pressure):
    if pressure < 980:
        return "Bardzo niskie ciśnienie - możliwe zmęczenie i bóle głowy."
    elif 980 <= pressure <= 1000:
        return "Niskie ciśnienie - możesz odczuwać senność."
    elif 1001 <= pressure <= 1015:
        return "Optymalne ciśnienie - stabilne samopoczucie."
    elif 1016 <= pressure <= 1030:
        return "Wysokie ciśnienie - możliwa poprawa nastroju."
    else:
        return "Bardzo wysokie ciśnienie - możliwy dyskomfort."

def display_weather(city, weather_data, date):
    weather_desc = weather_data['weather'][0]['description']
    temperature = round(weather_data['main']['temp'])
    feels_like = round(weather_data['main']['feels_like'])
    pressure = weather_data['main']['pressure']
    humidity = weather_data['main']['humidity']
    wind_speed = round(weather_data['wind']['speed'], 1)
    visibility = weather_data.get('visibility', None)
    
    visibility_info = format_visibility(visibility)
    pressure_info = format_pressure(pressure)
    
    print("-" * 50)
    print(f"Pogoda dla miasta: {city.capitalize()} ({date})")
    print(f"Opis: {weather_desc.capitalize()}")
    print(f"Temperatura: {temperature}°C (odczuwalna: {feels_like}°C)")
    print(f"Wilgotność: {humidity}%")
    print(f"Wiatr: {wind_speed} m/s")
    print(f"Ciśnienie: {pressure} hPa - {pressure_info}")
    print(visibility_info)
    print("-" * 50)

def main():
    API_KEY = "4c2deedf1d3d4ed1e5d30da8816e9308"
    actual_date = datetime.now().date()
    
    while True:
        city = input("Podaj nazwę miasta lub wpisz 'exit', aby zakończyć: ")
        if city.lower() == "exit":
            print("Koniec programu.")
            break
        
        choice = input("Czy chcesz prognozę na 5 dni? (tak/nie): ").strip().lower()
        
        if choice == "tak":
            forecast_data = get_forecast_data(city, API_KEY)
            if not forecast_data:
                continue
            
            print("Dostępne daty prognozy:")
            available_dates = set()
            for entry in forecast_data['list']:
                date = entry['dt_txt'].split(" ")[0]
                available_dates.add(date)
            
            for date in sorted(available_dates):
                print(date)
            
            selected_date = input("Wpisz datę (YYYY-MM-DD): ").strip()
            if selected_date not in available_dates:
                print("Niepoprawna data, spróbuj ponownie.")
                continue
            
            for entry in forecast_data['list']:
                if entry['dt_txt'].startswith(selected_date):
                    display_weather(city, entry, selected_date)
                    break
        else:
            weather_data = get_weather_data(city, API_KEY)
            if not weather_data:
                continue
            display_weather(city, weather_data, actual_date)
            
if __name__ == "__main__":
    main()
