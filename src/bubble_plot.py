# -*- coding:utf-8 -*-

"""
都道府県別の人口をバブルプロットする
参考URL（Qiita）
https://qiita.com/Hiroyuki1993/items/42861ff8b04c96005bc8
"""

import os
import glob
import json
import folium
import subprocess
import pandas as pd
import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt
from PIL import Image


inpath = '../data/e-stat'
incsv = r'男女別人口－全国，都道府県（大正９年～平成27年）.csv'

data = pd.read_csv(os.path.join(inpath, incsv), encoding='Shift-JIS',
                   skipfooter=2)

target_pref = data['都道府県名'].drop_duplicates()[1:48]
target_pref = ['北海道', '宮城県', '栃木県', '東京都', '愛知県',
               '大阪府', '香川県', '岡山県', '福岡県', '鹿児島県']

data_target = data[data['都道府県名'].str.contains('|'.join(target_pref))]

d = data_target[data_target['西暦（年）']==1920]

print('|'.join(target_pref))

c = np.arange(0, len(target_pref)*2, 2)
z = d['人口（総数）'].astype(int) / 1000
x = np.random.rand(len(target_pref))
y = np.random.rand(len(target_pref))

plt.figure(figsize=(10, 8))
plt.scatter(x, y, s=z, alpha=0.5, c=c)
for i, t in enumerate(target_pref):
    plt.text(x[i], y[i], t, fontsize=15)

# plt.show()

# 年ごとにアニメーション
data_target['人口（総数）'] = data_target['人口（総数）'].replace('-', 0)
df_loc_pref = pd.read_json('./loc_pref.json').T
x = df_loc_pref.loc[target_pref, 'longitude']
y = df_loc_pref.loc[target_pref, 'latitude']

for year in range(1920, 2016, 5):
    z = data_target[data_target['西暦（年）']==year]['人口（総数）'].astype(int) / 1000
    plt.figure()
    plt.scatter(x, y, s=z, alpha=0.3, c=c)
    for i, t in enumerate(target_pref):
        plt.text(x[i], y[i], t, fontsize=10)
    plt.xlim((125, 145))
    plt.ylim((28, 45))
    plt.title('{0}年の人口'.format(year))
    plt.savefig('../output/bubble_{0}.png'.format(year))
    plt.close()

    # foliumを使って描画する
    m = folium.Map(location=[34.7, 135.2], zoom_start=5)
    z = z.reset_index(drop=True)

    for i, t in enumerate(target_pref):
        folium.CircleMarker(
            location=[y[i], x[i]],
            radius=z[i] / 100,
            popup=t,
            color='#3186cc',
            fill_color='#3186cc'
        ).add_to(m)
    m.save('../output/folium_{0}.html'.format(year))

# 保存したPNGを読み込んでGIFを作成する
bubbles = []
files = os.listdir('../output/')
files.sort()

for file in files:
    if os.path.splitext(file)[1] == '.png':
        im = Image.open('../output/' + file)
        bubbles.append(im)

bubbles[0].save('../output/bubble.gif', save_all=True, append_images=bubbles[1:],
                duration=1000)




