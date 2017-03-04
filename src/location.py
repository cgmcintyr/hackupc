import json
import os
from shapely.geometry import shape, Point

this_dir = os.path.dirname(os.path.abspath(__file__))

with open(os.path.join(this_dir, 'spain-provinces.geojson')) as f:
    regions = json.load(f)

def get_province_code(lon, lat):
    point = Point(lon, lat)
    for feature in regions['features']:
        polygon = shape(feature['geometry'])
        if polygon.contains(point):
            return feature['properties']['cod_prov']
    return None
