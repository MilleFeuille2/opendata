# -*- encoding:utf-8 -*-
"""
参考URL
https://qiita.com/momota10/items/3b878f01d489a32e40c3
"""

import folium


# 東京駅の位置
m = folium.Map(location=[35.681382, 139.766083], zoom_start=14)

folium.Marker([35.658581, 139.745433], popup='Tokyo tower', icon=folium.Icon(color='blue')).add_to(m)
folium.Marker([35.710063, 139.8107], popup='Tokyo skytree', icon=folium.Icon(color='blue', icon='bookmark')).add_to(m)

folium.CircleMarker(
    location=[35.681382, 139.76608399999998],
    radius=200,
    popup='Tokyo Station',
    color='#3186cc',
    fill_color='#3186cc'
).add_to(m)


m.save('../output/folium.html')

