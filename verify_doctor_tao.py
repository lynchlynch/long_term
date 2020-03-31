import time
import pandas as pd
from multiprocessing import Pool
import os
import numpy as np

import select_rps as sr
import new_yearly_high_price as nyhp

stock_path = 'D:/pydir/Raw Data/Tushare_pro/daily_data/'
# stock_path = '/Users/pei/PycharmProjects/Raw Data/Tushare_pro/daily_data/'
report_path = 'D:/pydir/Raw Data/Report/PerReport'
# report_path = '/Users/pei/PycharmProjects/Raw Data/Report/PerReport'
result_path = 'D:/pydir/docter_tao/result'
# result_path = '/Users/pei/PycharmProjects/docter_tao/result'

start_time = time.time()

rps_N1 = 50
stock_length = 500
current_process_date = 20200331
rps_N2 = 120
rps_N3 = 250
high_price_threshold = 0.9
# rps_threshold_list = [45, 45, 45]
rps_threshold_list = [80, 80, 80]

# 获取前一个交易日的日期
data_orgin_1 = pd.read_csv(stock_path + '/000001.csv')
current_date_index_1 = data_orgin_1[data_orgin_1['trade_date'] == current_process_date].index.tolist()[0]
pre_date_1 = data_orgin_1['trade_date'][current_date_index_1 - 1]
data_orgin_2 = pd.read_csv(stock_path + '/000002.csv')
current_date_index_2 = data_orgin_2[data_orgin_2['trade_date'] == current_process_date].index.tolist()[0]
pre_date_2 = data_orgin_2['trade_date'][current_date_index_2 - 1]
data_orgin_3 = pd.read_csv(stock_path + '/000004.csv')
current_date_index_3 = data_orgin_3[data_orgin_3['trade_date'] == current_process_date].index.tolist()[0]
pre_date_3 = data_orgin_3['trade_date'][current_date_index_3 - 1]
if pre_date_1 == pre_date_2 or pre_date_1 == pre_date_3:
    pre_date = pre_date_1
elif pre_date_2 == pre_date_3:
    pre_date = pre_date_2
else:
    data_orgin_4 = pd.read_csv(stock_path + '/000005.csv')
    current_date_index_4 = data_orgin_4[data_orgin_4['trade_date'] == current_process_date].index.tolist()[0]
    pre_date_4 = data_orgin_4['trade_date'][current_date_index_4 - 1]
    if pre_date_4 == pre_date_1 or pre_date_4 == pre_date_2 or pre_date_4 == pre_date_3:
        pre_date = pre_date_4


rps_df, rps_df_above_theshold = sr.rps_sorted(stock_path, rps_N1, stock_length, current_process_date)

stock_code_df = sr.rps_reverse(stock_path, rps_df_above_theshold, current_process_date)
# 计算120,250的rps
rps_df2, rps_df_above_theshold2 = sr.rps_sorted(stock_path, rps_N2, stock_length, current_process_date)
rps_df3, rps_df_above_theshold3 = sr.rps_sorted(stock_path, rps_N3, stock_length, current_process_date)
rps_df3_pre, rps_df_above_theshold3 = sr.rps_sorted(stock_path, rps_N3, stock_length, pre_date)

