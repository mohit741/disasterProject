import os

from django.http import JsonResponse

from disasterProject.settings import BASE_DIR
from django.shortcuts import render, redirect
from cope_with_disaster.fb_auto_post import post_warning
import requests
import json
from .forms import EmailSubForm, UserForm, RegForm
from .models import Variable, Rescuer
from django.contrib.auth import login, authenticate, logout


# Utility functions
# Weather widget
def get_weather_info(place):
    url = 'http://api.openweathermap.org/data/2.5/weather?q={}&units=metric&appid=aa1e682c3c12647a0b9f91aacd0397cf'
    city_weather = requests.get(url.format(place)).json()
    return city_weather


def get_weather_info_lat_lon(lat, lon):
    url = 'http://api.openweathermap.org/data/2.5/weather?lat={}&lon={}&units=metric&appid=aa1e682c3c12647a0b9f91aacd0397cf'
    city_weather = requests.get(url.format(lat, lon)).json()
    return city_weather


# Flood Danger zones
def get_danger_zones():
    fp = os.path.join(BASE_DIR, 'cope_with_disaster/json_data/flood_zones.json')
    zones = json.load(open(fp))
    return zones


# Warning from predictions
def get_warning():
    flag = Variable.objects.filter(name='FAKE_WARNING').first().info
    if flag == 'true':
        return True
    else:
        return False


# Get dam list
def get_stations(state):
    fp = os.path.join(BASE_DIR, 'cope_with_disaster/json_data/' + state + '_geo.json')
    stations = json.load(open(fp))
    return stations


# Home
def home(request):
    data = dict()
    # city = City.objects.filter(name='New Delhi').first()
    data['winfo'] = get_weather_info('New Delhi')
    if get_warning():
        data['warn'] = 'There is a report of flood in FAKE AREA, stay alert and connected with us for more information'

    zones = get_danger_zones()
    return render(request, 'flood_home.html', {'data': data, 'zones': zones})

def register_user(request):
    if request.method == 'POST':
        user_form = UserForm(request.POST)
        dform = RegForm(request.POST)
        if user_form.is_valid():
            user_form.save()
            username = user_form.cleaned_data.get('email')
            raw_password = user_form.cleaned_data.get('password1')
            user = authenticate(email=username, password=raw_password)
            profile = Rescuer.objects.get(user=user)
            dform = RegForm(request.POST, instance=profile)
            dform.save()
            login(request, user)
            return redirect('/floods')
    else:
        user_form = UserForm()
        dform = RegForm()
    return render(request, 'register.html', {'user_form': user_form, 'dform': dform})


def user_login(request):
    err=''
    if request.method=='POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('/floods', {'user': user})
        err = 'User credentials not valid!'
        return render(request, 'login_user.html', {'err': err})
    else:
        return render(request, 'login_user.html', {'err': err})


def register_query(request):
    return render(request, 'volunteer.html')

def stats(request):
    return render(request, 'current_stats.html')


def undev(request):
    return render(request, 'undev.html')


def subscribe(request):
    if request.method == 'POST':
        form = EmailSubForm(request.POST)
        print(form)
        if form.is_valid():
            x = form.save()
            print(x)
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
    elif state == 'UP':
        state = 'Uttar Pradesh'
    data = dict()
    fp = os.path.join(BASE_DIR, 'cope_with_disaster/json_data/capitals.json')
    capitals = json.load(open(fp))
    data['winfo'] = get_weather_info(capitals[state])
    print(data['winfo'])
    stations = get_stations(state)
    return render(request, 'state_stats.html',
                  {'data': data, 'stations': stations, 'state': state, 'city': capitals[state]})


def stations_view(request, state, code):
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
    elif state == 'UP':
        state = 'Uttar Pradesh'
    fp = os.path.join(BASE_DIR, 'cope_with_disaster/json_data/' + state + '_geocoded.json')
    d = json.load(open(fp))
    path = str(state + '/' + d[int(code)]['name'])
    imgpath = 'images/{}.png'.format(path)
    sname = d[int(code)]['name']
    winfo = get_weather_info_lat_lon(d[int(code)]['lat'], d[int(code)]['lon'])
    return render(request, 'station.html', {'imgpath': imgpath, 'sname': sname, 'winfo': winfo, 'state': state})


def predict(request):
    return render(request, 'flood_predictions.html')


def logout_user(request):
    logout(request)
    return redirect('/floods')


def about(request):
    return render(request, 'about.html')


def get_loc_stats(request):
    lat = request.GET['lat']
    lon = request.GET['lon']
    print(lat+lon)
    data = {'tweets':'0'}
    return JsonResponse(data)

def get_predicted_locations(request):
    fp = os.path.join(BASE_DIR, 'cope_with_disaster/json_data/' + 'predictions.json')
    data = json.load(open(fp))
    return JsonResponse(data)


def get_current_loc(request):
    user = request.user
    lat = float(Rescuer.objects.filter(user=user).first().lat)
    lon = float(Rescuer.objects.filter(user=user).first().lon)
    data = {'lat':lat, 'lon':lon}
    return JsonResponse(data)

def set_current_loc(request):
    user = request.user
    resc = Rescuer.objects.get(user=user)
    print('Old',resc.lat)
    resc.lat = float(request.GET['lat'])
    resc.lon = float(request.GET['lon'])
    resc.save()
    return JsonResponse({'status':'sucess'})

def control_center(request):
    return render(request,'control.html')

def get_markers_pos(request):
    data = {}
    mode = request.GET['mode']
    typ = request.GET['type']
    fp = os.path.join(BASE_DIR, 'cope_with_disaster/json_data/' + mode + '.json')
    d = json.load(open(fp))
    data['results'] = d[str(typ)]
    return JsonResponse(data)
