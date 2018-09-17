# -*- coding:utf-8 -*-

import pandas as pd


input_path = r'../csv/df.csv'

df_input = pd.read_csv(input_path, index_col=0)

df_output = df_input['odpt:railway'].drop_duplicates()

df_output.to_csv('../csv/df_drop_duplicates.csv')
