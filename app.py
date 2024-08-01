from flask import Flask, render_template, request
import requests
from datetime import date
from dataclasses import dataclass

app = Flask(__name__)
Api_key = "c153237666e0506f57984ac136d610b8"

@dataclass
class WeatherData: 
    main: str
    description: str
    icon: str
    wind_speed: float
    curr_temperature: float
    min_temperature: float
    max_temperature: float
    name: str

def current_city(city_name):
    resp = requests.get(f'https://api.openweathermap.org/data/2.5/weather?q={city_name}&appid={Api_key}&units=metric').json()
        
    current = WeatherData(
        main = resp.get('weather')[0].get('main'),
        description = resp.get('weather')[0].get('description'),
        icon = resp.get('weather')[0].get('icon'),
        wind_speed = resp.get('wind').get('speed'),
        curr_temperature = resp.get('main').get('temp'),
        min_temperature = resp.get('main').get('min_temp'),
        max_temperature = resp.get('main').get('max_temp'),
        name = resp.get('name'),
    ) 
    return current

def get_current(city_name):        
    try:
         response = requests.get(f'https://api.openweathermap.org/data/2.5/weather?q={city_name}&appid={Api_key}&units=metric')
         response.raise_for_status()  # Raises an exception if the response was not successful
         resp = response.json()
         data = WeatherData(
            main = resp.get('weather')[0].get('main'),
            description = resp.get('weather')[0].get('description'),
            icon = resp.get('weather')[0].get('icon'),
            wind_speed = resp.get('wind').get('speed'),
            curr_temperature = resp.get('main').get('temp'),
            min_temperature = resp.get('main').get('min_temp'),
            max_temperature = resp.get('main').get('max_temp'),
            name = resp.get('name'),
            )
         return data
    except requests.exceptions.HTTPError as errh:
         print(f"HTTP Error: {errh}")
    except requests.exceptions.ConnectionError as errc:
         print(f"Error Connecting: {errc}")
    except requests.exceptions.Timeout as errt:
         print(f"Timeout Error: {errt}")
    except requests.exceptions.RequestException as err:
         print(f"Something went wrong: {err}")


def get_forecast(city_name):        
    try:
        resp = requests.get(f'https://api.openweathermap.org/data/2.5/forecast?q={city_name}&appid={Api_key}&units=metric').json()
        forecast = resp
        hourly_forecast = forecast['list'][:12]
        return hourly_forecast
    except requests.exceptions.HTTPError as errh:
         print(f"HTTP Error: {errh}")
    except requests.exceptions.ConnectionError as errc:
         print(f"Error Connecting: {errc}")
    except requests.exceptions.Timeout as errt:
         print(f"Timeout Error: {errt}")
    except requests.exceptions.RequestException as err:
         print(f"Something went wrong: {err}")

@app.route('/', methods=['GET', 'POST'])
def index():
    data = None
    forecast = None
    if request.method == 'POST':
        if request.form['cityName']:
            city = request.form['cityName']
            data = get_current(city)
            # forecast = get_forecast(city)
            print(forecast)
        else: 
            post_e_msg = "Please enter a valid city name"
            print(post_e_msg)
        
    today = date.today()
    print("Today's date:", today)
    current = current_city("Cape Town")
    return render_template("index.html", today = today, data = data, forecast = forecast, current = current)

if __name__ == "__main__":
    app.run(debug=True)