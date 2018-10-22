"""This snippet converts normal JSON file with latitude and longitude data
   to GeoJSON format which can be used with maps APIs"""


from sys import argv
from os.path import exists
import json

k = json.load(open('json_data/dams.json'))
geojson = dict()
"""for d in k:
    if k[d]['deaths'] > 150:
        data[d] = k[d]"""

for key in k:
    geojson[key] = {
        "type": "FeatureCollection",
        "features": [
            {
                "type": "Feature",
                "geometry": {
                    "type": "Point",
                    "coordinates": [d["lon"], d["lat"]],
                },
                "properties": {
                    "name": d["name"],
                    "river": d["river"]
                },
            } for d in k[key]]
    }
output = open('json_data/dams_zones.json', 'w')
json.dump(geojson, output)
