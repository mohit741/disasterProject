"""This snippet converts normal JSON file with latitude and longitude data
   to GeoJSON format which can be used with maps APIs"""

from sys import argv
from os.path import exists
import json

states = ['West Bengal', 'Tamil Nadu', 'Uttar Pradesh', 'Rajasthan', 'Kerala', 'Maharashtra', 'Madhya Pradesh',
          'Karnataka', 'Jammu & Kashmir', 'Himachal Pradesh']
# k = json.load(open('json_data/dams.json'))
# geojson = dict()
"""for d in k:
    if k[d]['deaths'] > 150:
        data[d] = k[d]"""
for state in states:
    df = json.load(open(state + '_geocoded.json'))
    geojson = {
        "type": "FeatureCollection",
        "features": [
            {
                "type": "Feature",
                "geometry": {
                    "type": "Point",
                    "coordinates": [df[d]["lon"], df[d]["lat"]],
                },
                "properties": {
                    "name": df[d]["name"],
                    "code": df[d]["code"]
                },
            } for d in range(0, len(df))]
    }
    output = open(state + '_geo.json', 'w')
    json.dump(geojson, output)
