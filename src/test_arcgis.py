# -*- coding:utf-8 -*-

from arcgis.gis import GIS

gis = GIS()
map = gis.map("東京都", zoomlevel = 13)

map.draw(shape=(10, 10))

print(map)
