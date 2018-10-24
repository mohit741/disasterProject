import os
from disasterProject.settings import BASE_DIR
from django.shortcuts import render, redirect
from cope_with_disaster.fb_auto_post import post_warning
import requests
import json
from .forms import EmailSubForm


# Utility functions
# Weather widget
def get_weather_info(place):
    # url = 'http://api.openweathermap.org/data/2.5/weather?lat={}&lon={}&units=metric&appid=aa1e682c3c12647a0b9f91aacd0397cf'
    url = 'http://api.openweathermap.org/data/2.5/weather?q={}&units=metric&appid=aa1e682c3c12647a0b9f91aacd0397cf'
    city_weather = requests.get(url.format(place)).json()
    return city_weather


# Flood Danger zones
def get_danger_zones():
    fp = os.path.join(BASE_DIR, 'cope_with_disaster/json_data/flood_zones.json')
    zones = json.load(open(fp))
    return zones


# Warning from predictions
def get_warning():
    pass


# Get dam list
def get_dams(state):
    fp = os.path.join(BASE_DIR, 'cope_with_disaster/json_data/dams_zones.json')
    dams = json.load(open(fp))
    try:
        dlist = dams[state]
    except KeyError:
        dlist = []
    return dlist


# Home
def home(request):
    data = dict()
    # city = City.objects.filter(name='New Delhi').first()
    data['winfo'] = get_weather_info('New Delhi')
    data['test'] = post_warning()
    print(data['winfo'])
    # data['warning'] = get_warning()
    zones = get_danger_zones()
    return render(request, 'flood_home.html', {'data': data, 'zones': zones})


def stats(request):
    return render(request, 'current_stats.html')


def undev(request):
    return render(request, 'undev.html')

def subscribe(request):
    if request.method == 'POST':
        form = EmailSubForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('/floods')
        else:
            return redirect('/subscribe', {'error': 'Error Occured '})
    else:
        form = EmailSubForm()
        return render(request, 'subscribe.html', {'form': form})



def state_info(request, state):
    if state == 'JandK':
        state = 'Jammu and Kashmir'
    elif state == 'WB':
        state = 'West Bengal'
    elif state == 'AP':
        state = 'Andhra Pradesh'
    elif state == 'MP':
        state = 'Madhya Pradesh'
    elif state == 'TN':
        state = 'Tamil Nadu'
    elif state == 'HP':
        state = 'Himachal Pradesh'
    data = dict()
    data['winfo'] = get_weather_info(state)
    print(data['winfo'])
    dams = get_dams(state)
    return render(request, 'state_stats.html', {'data': data, 'dams': dams, 'state': state})


def predict(request):
    return render(request, 'flood_predictions.html')
