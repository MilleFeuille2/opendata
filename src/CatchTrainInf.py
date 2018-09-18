# -*- coding:utf-8 -*-

""" 東京メトロのAPIで運行情報をjson形式で取得する """

import json
import urllib.parse
import urllib.request
import pandas as pd
import trainname
#####
# sslでエラーが出る。証明書の問題？ セキュリティー上あんま良くないと思う
import ssl
ssl._create_default_https_context = ssl._create_unverified_context
#####


def train_info():

    endpoint = 'https://api-tokyochallenge.odpt.org'
    API_TYPE = '/api/v4/'
    rdf_type = 'Train'
    API_KEY = ''
    request_url = endpoint + API_TYPE + 'odpt:' + rdf_type + '?' + 'acl:consumerKey=' + API_KEY

    response = urllib.request.urlopen(request_url)
    # text = response.read().decode()
    text = response.read()
    df = pd.DataFrame.from_records(json.loads(text))

    # print(df)
    df.to_csv('../csv/df.csv')

    return text


def train_info_top(target=None):
    # 運行情報を取得
    # jsonをstrに変換して格納
    infdata = json.loads(train_info())

    result = []

    for inf in infdata:

        # if inf["odpt:railway"] == trainname.train_name(target):

        # 生データ（デバッグの時とかに見る）
        # print(inf)

        # 情報公開日時のフォーマット処理
        date = inf["dc:date"]
        date = date.split("T")
        date[1] = date[1].split("+")
        date = date[0] + ";" + date[1][0]

        result.append({
            "line": trainname.train_name(inf["odpt:railway"], True),
            "presentationTime": date,
            "destination": inf["odpt:destinationStation"][0],
            "from": inf["odpt:fromStation"]
            })

    return result


if __name__ == '__main__':

    # print(train_info_top("常磐線"))
    result = train_info_top()

    for i in range(len(result)):
        print(result[i])


