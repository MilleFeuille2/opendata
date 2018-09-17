# -*- coding:utf-8 -*-
"""
参考URL
https://qiita.com/aimof/items/b4e4551d27abaf5bb258
"""
import osmnx as ox
import matplotlib.pyplot as plt


shinjuku = ox.graph_from_place('Shinjuku')

ox.plot_graph(ox.project_graph(shinjuku))