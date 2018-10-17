from django.shortcuts import render
import requests


# Weather widget
def get_weather_info(city):
    url = 'http://api.openweathermap.org/data/2.5/weather?q={}&units=imperial&appid=aa1e682c3c12647a0b9f91aacd0397cf'
    city_weather = requests.get(url.format(city)).json()
    return city_weather


# Home
def home(request):
    return render(request, 'flood_home.html')