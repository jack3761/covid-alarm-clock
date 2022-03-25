import json
import requests
import pyttsx3


with open('config.json', 'r') as f:
    x = json.load(f)["weather"]
    api_key = x["weather_key"]
    base_url = x["weather_URL"]    
    city_name = x["weather_city"]
    
complete_url = base_url + "appid=" + api_key + "&q=" + city_name
# print response object
response = requests.get(complete_url)
x = response.json()
y = x["main"]
current_temperature = y["temp"]
current_feels_like = y["feels_like"]
celcius = round(current_temperature - 273.1)
feels_like_celcius = round(current_feels_like - 273.1)
current_pressure = y["pressure"]
current_humidiy = y["humidity"]
z = x["weather"]
weather_description = z[0]["description"]
	
    
        
def get_weather():
    celcius = round(current_temperature - 273.1)
    return [celcius, weather_description, city_name]