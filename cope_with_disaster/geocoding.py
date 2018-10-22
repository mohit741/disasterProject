# Python script to geocode given data
# Author : Mohit Kumar
import requests
import json
import time
import pandas as pd

GOOGLE_MAPS_API_URL = 'https://maps.googleapis.com/maps/api/geocode/json'

params = {
    'address': 'Jharkhand',
    'sensor': 'false',
    'key': 'AIzaSyCcHofqZ7qVRGDmAOFyJK9ufcjJow6fFEU'
}

# df = pd.read_json('json_data/flood_data.json')
df = json.load(open('json_data/dam.json'))
geodata = dict()
# Do the request and get the response data
t = 0
for key in df:
    l = list()
    for i in range(0, len(df[key])):
        params['address'] = str(df[key][i]['name']) + ' dam'
        req = requests.get(GOOGLE_MAPS_API_URL, params=params)
        res = req.json()
        try:
            result = res['results'][0]
        except IndexError:
            continue
        d = dict()
        d['lat'] = result['geometry']['location']['lat']
        d['lon'] = result['geometry']['location']['lng']
        d['name'] = df[key][i]['name']
        try:
            d['river'] = df[key][i]['River']
        except KeyError:
            d['river'] = ''
        l.append(d)
        t += 1
        print(t)
    geodata[key] = l
    time.sleep(0.1)
json.dump(geodata, open('json_data/dams.json', 'w'))
"""for key in df:
    params['address'] = str(key).capitalize()
    req = requests.get(GOOGLE_MAPS_API_URL, params=params)
    res = req.json()
    result = res['results'][0]
    d = dict()
    d['lat'] = result['geometry']['location']['lat']
    d['lon'] = result['geometry']['location']['lng']
    d['deaths'] = df[key]['Grand Total']
    geodata[str(key).capitalize()] = d

pd.DataFrame(geodata).to_json('json_data/states.json')"""
