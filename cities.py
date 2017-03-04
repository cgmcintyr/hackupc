# -*- coding: utf-8 -*-

from collections import namedtuple

City = namedtuple('City', ['name', 'province', 'population', 'latitude', 'longitude'])

cities = [City("Madrid", "Madrid", 3255944, 40.417 , -3.703),
          City("Barcelona", "Catalonia,", 1621537, 41.389, 2.159),
          City("Valencia", "Valencia,", 814208, 39.47, -0.377),
          City("Seville", "Andalusia,", 703206,37.383, -5.973),
          City("Zaragoza", "Aragon,", 674317, 41.656, -0.877),
          City("Málaga", "Andalusia", 568305, 36.72, -4.42),
          City("Murcia", "Murcia,", 436870, 37.987, -1.13),
          City("Palma", "Balearic Islands", 401270, 39.569, 2.65),
          City("Las Palmas de Gran Canaria", "Canary Islands", 381847, 28.1, -15.413),
          City("Bilbao", "Basque Country", 354860, 43.263, -2.925),
]
