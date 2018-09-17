# -*- coding:utf-8 -*-

import psycopg2
import pandas as pd


def train_name(s, has_id):

    # DB接続情報
    conn = psycopg2.connect('dbname=odpt host=localhost user=postgres password=postgres')
    cur = conn.cursor()

    if has_id:
        s = s.replace('odpt.Railway:', '')

        sql = 'select * ' \
              'from mst_railway ' \
              'where railway = \'{0}\''.format(s)

    else:
        # sql =
        pass

    result = pd.read_sql(sql=sql, con=conn, index_col=None)

    print(result['railway_jp'].values[0])

    return result['railway_jp'].values[0]