# -*- coding:utf-8 -*-

""" 東京公共交通オープンデータを取得する """

import json
import folium
import urllib
import urllib.parse
import urllib.request
import pandas as pd
# import geopandas as gpd
import matplotlib.pyplot as plt
import trainname
import busname
import airplanename
import odpt_apikey


def search_info(rdf_type, predicate=None):
    """ データ検索API """
    if predicate:
        request_url = endpoint + API_TYPE + 'odpt:' + rdf_type + '?' +\
                      predicate + '&' +\
                      'acl:consumerKey=' + API_KEY
    else:
        request_url = endpoint + API_TYPE + 'odpt:' + rdf_type + '?' +\
                      'acl:consumerKey=' + API_KEY

    response = urllib.request.urlopen(request_url)
    # text = response.read().decode()
    text = response.read().decode('utf-8')
    df = pd.DataFrame.from_records(json.loads(text))
    df.to_csv('../csv/df_{0}.csv'.format(rdf_type))

    return text


def dump_info(rdf_type):
    """ データダンプAPI """
    request_url = endpoint + API_TYPE + 'odpt:' + rdf_type + '.json?' + 'acl:consumerKey=' + API_KEY

    response = urllib.request.urlopen(request_url)
    # text = response.read().decode()
    text = response.read()
    df = pd.DataFrame.from_records(json.loads(text))
    df.to_csv('../csv/df_{0}.csv'.format(rdf_type))

    return text


def get_info(rdf_type):
    """ データ取得API """
    urn = ''
    request_url = endpoint + API_TYPE + 'datapoints/' + urn + '?' + 'acl:consumerKey=' + API_KEY

    response = urllib.request.urlopen(request_url)
    # text = response.read().decode()
    text = response.read()
    df = pd.DataFrame.from_records(json.loads(text))
    df.to_csv('../csv/df_{0}.csv'.format(rdf_type))

    return text


def search_loc(rdf_type):
    """ 地物情報検索API """
    lon = '139.766926'  # 取得範囲の中心緯度
    lat = '35.681265'  # 取得範囲の中心軽度
    radius = '1000'  # 取得範囲の半径（m）0〜4000
    request_url = endpoint + API_TYPE + 'places/odpt:' + rdf_type +\
                  "?lon=" + lon + "&lat=" + lat + "&radius=" + radius + "&acl:consumerKey=" + API_KEY

    response = urllib.request.urlopen(request_url)
    # text = response.read().decode()
    text = response.read()
    df = pd.DataFrame.from_records(json.loads(text))
    df.to_csv('../csv/df_{0}.csv'.format(rdf_type))

    return text


def train_info_top(method, target):
    result = []

    # API取得
    if method == 'search':
        infdata = json.loads(search_info(target))
    elif method == 'dump':
        infdata = json.loads(dump_info(target))
    else:
        return result

    for inf in infdata:

        # if inf["odpt:railway"] == trainname.train_name(target):

        # 生データ（デバッグの時とかに見る）
        if target == 'Railway':
            print(inf)

        # 情報公開日時のフォーマット処理
        date = inf["dc:date"]
        date = date.split("T")
        date[1] = date[1].split("+")
        date = date[0] + ";" + date[1][0]

        if target == 'Train':
            result.append({
                "line": trainname.train_name(inf["odpt:railway"], True),
                "presentationTime": date,
                "destination": inf["odpt:destinationStation"][0],
                "from": inf["odpt:fromStation"]
                })

        elif target == 'PassengerSurvey':
            result.append({
                # 'date': date,
                'station_id': inf['odpt:station'][0],
                # 'railway_id': inf['odpt:railway'][0],
                'passenger': inf['odpt:passengerSurveyObject'][0]
            })

        elif target == 'Railway':
            if 'ug:region' in inf.keys():
                result.append({
                    # 'date': date,
                    'railway_id': inf['owl:sameAs'],
                    'railway_title': inf['odpt:railwayTitle'],
                    'color': inf['odpt:color'],
                    'loc': inf['ug:region']
                 })

        elif target == 'Station':
            if 'geo:long' in inf.keys() and 'geo:lat' in inf.keys() and\
               'odpt:passengerSurvey' in inf.keys():
                result.append({
                    # 'date': date,
                    'sameas': inf['owl:sameAs'],
                    'station_title': inf['odpt:stationTitle'],
                    'operator_id': inf['odpt:operator'],
                    'railway_id': inf['odpt:railway'],
                    'long': inf['geo:long'],
                    'lat': inf['geo:lat'],
                    # 'passenger': inf['odpt:passengerSurvey']
                })

        df_result = pd.DataFrame(result)

    return df_result


def bus_info_top(target=None):
    # 運行情報を取得
    # jsonをstrに変換して格納
    infdata = json.loads(search_info('Bus'))

    result = []

    for inf in infdata:

        # 生データ（デバッグの時とかに見る）
        # print(inf)

        # 情報公開日時のフォーマット処理
        date = inf["dc:date"]
        date = date.split("T")
        date[1] = date[1].split("+")
        date = date[0] + ";" + date[1][0]

        result.append({
            "busroute": inf["odpt:busroute"],
            "presentationTime": date
            })

    return result


def airplane_info_top(target=None):
    # 運行情報を取得
    # jsonをstrに変換して格納
    infdata = json.loads(search_info('FlightInformationArrival'))

    result = []

    for inf in infdata:

        # 生データ（デバッグの時とかに見る）
        # print(inf)

        # 情報公開日時のフォーマット処理
        date = inf["dc:date"]
        date = date.split("T")
        date[1] = date[1].split("+")
        date = date[0] + ";" + date[1][0]

        result.append({
            "presentationTime": date,
            "airline": inf['odpt:airline'],
            "flightNumber": inf['odpt:flightNumber'],
            "estimatedTime": inf['odpt:estimatedTime'],
            "scheduledTime": inf['odpt:scheduledTime'],
            "departureAirport": inf['odpt:departureAirport'],
            "destinationAirport": inf['odpt:destinationAirport']
            })

    return result


def map_station(df):
    # 1つ目の駅を基準にする
    lat = df.loc[0, 'lat']
    long = df.loc[0, 'long']

    m = folium.Map([lat, long], zoom_start=10)

    # 中身確認用
    # print(df.head())

    for i in range(len(df)):
        folium.CircleMarker(
            location=[df.loc[i, 'lat'], df.loc[i, 'long']],
            radius=1,
            popup=df.loc[i, 'station_title']['ja'],
            color='#000000',
            fill_color='#000000'
        ).add_to(m)

    m.save('../output/folium_station.html')
    return m


def map_passenger(m, df_sta, df_pas):

    df_color = pd.read_json('./traincolor.json').T
    df = pd.merge(df_sta, df_pas, left_on='sameas', right_on='station_id')
    df = pd.merge(df, df_color, on='railway_id')

    # 1つ目の駅を基準にする
    lat = df.loc[0, 'lat']
    long = df.loc[0, 'long']

    # foliumを使う
    # m = folium.Map([lat, long], zoom_start=10)

    for i in range(len(df)):
        folium.CircleMarker(
            location=[df.loc[i, 'lat'], df.loc[i, 'long']],
            radius=df.loc[i, 'passenger']['odpt:passengerJourneys'] / 10**4,
            popup=df.loc[i, 'station_title']['ja'],
            color=df.loc[i, 'color'],
            fill_color=df.loc[i, 'color']
        ).add_to(m)

    m.save('../output/folium_passenger.html')

    # # geopandasを使う
    # df_tokyo = gpd.read_file('../land/tokyo.geojson')
    # ax = df_tokyo[df_tokyo['area_en'] == 'Tokubu'].plot()
    # ax.scatter(df['long'], df['lat'], color='r')
    # plt.savefig('../output/geopandas_passenger.png')

    return m


if __name__ == '__main__':

    endpoint = 'https://api-tokyochallenge.odpt.org'
    API_TYPE = '/api/v4/'
    API_KEY = odpt_apikey.api_key()

    df_sta = train_info_top('dump', 'Station')
    df_pas = train_info_top('dump', 'PassengerSurvey')
    # df_rai = train_info_top('search', 'Railway')

    # print(df_rai.head())

    # result = bus_info_top()

    # result = airplane_info_top()
    # result = search_loc('Station')
    
    # for i in range(len(result)):
    #     print(result[i])

    m = map_station(df_sta)

    map_passenger(m, df_sta, df_pas)
