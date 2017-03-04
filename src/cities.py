# -*- coding: utf-8 -*-

from collections import namedtuple
import math

City = namedtuple('City', ['name', 'province', 'population', 'latitude', 'longitude', 'bounding'])

# degrees to radians
def deg2rad(degrees):
    return math.pi*degrees/180.0
# radians to degrees
def rad2deg(radians):
    return 180.0*radians/math.pi

# Semi-axes of WGS-84 geoidal reference
WGS84_a = 6378137.0  # Major semiaxis [m]
WGS84_b = 6356752.3  # Minor semiaxis [m]

# Earth radius at a given latitude, according to the WGS-84 ellipsoid [m]
def WGS84EarthRadius(lat):
    # http://en.wikipedia.org/wiki/Earth_radius
    An = WGS84_a*WGS84_a * math.cos(lat)
    Bn = WGS84_b*WGS84_b * math.sin(lat)
    Ad = WGS84_a * math.cos(lat)
    Bd = WGS84_b * math.sin(lat)
    return math.sqrt( (An*An + Bn*Bn)/(Ad*Ad + Bd*Bd) )

# Bounding box surrounding the point at given coordinates,
# assuming local approximation of Earth surface as a sphere
# of radius given by WGS84
def boundingBox(latitudeInDegrees, longitudeInDegrees, halfSideInKm):
    lat = deg2rad(latitudeInDegrees)
    lon = deg2rad(longitudeInDegrees)
    halfSide = 1000*halfSideInKm

    # Radius of Earth at given latitude
    radius = WGS84EarthRadius(lat)
    # Radius of the parallel at given latitude
    pradius = radius*math.cos(lat)

    latMin = lat - halfSide/radius
    latMax = lat + halfSide/radius
    lonMin = lon - halfSide/pradius
    lonMax = lon + halfSide/pradius

    return (rad2deg(latMin), rad2deg(lonMin), rad2deg(latMax), rad2deg(lonMax))

boundBoxSize = 100

names = ["madrid", "barcelona", "valencia", "seville", "zaragoza", 
         "málaga", "murcia", "palma", "las palmas de gran canaria", "bilbao"]

data  = [City("Madrid", "Madrid", 3255944, 40.417 , -3.703, boundingBox(40.417 , -3.703, boundBoxSize)),
         City("Barcelona", "Catalonia,", 1621537, 41.389, 2.159, boundingBox(41.389, 2.159, boundBoxSize)),
         City("Valencia", "Valencia,", 814208, 39.47, -0.377, boundingBox(39.47, -0.377, boundBoxSize)),
         City("Seville", "Andalusia,", 703206, 37.383, -5.973, boundingBox(37.383, -5.973, boundBoxSize)),
         City("Zaragoza", "Aragon,", 674317, 41.656, -0.877, boundingBox(41.656, -0.877, boundBoxSize)),
         City("Málaga", "Andalusia", 568305, 36.72, -4.42, boundingBox(36.72, -4.42, boundBoxSize)),
         City("Murcia", "Murcia,", 436870, 37.987, -1.13, boundingBox(37.987, -1.13, boundBoxSize)),
         City("Palma", "Balearic Islands", 401270, 39.569, 2.65, boundingBox(39.569, 2.65, boundBoxSize)),
         City("Las Palmas de Gran Canaria", "Canary Islands", 381847, 28.1, -15.413, boundingBox(28.1, -15.413, boundBoxSize)),
         City("Bilbao", "Basque Country", 354860, 43.263, -2.925, boundingBox(43.263, -2.925, boundBoxSize)),
]

cities = dict(zip(names,data))
