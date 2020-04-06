import time
import pandas as pd
from multiprocessing import Pool
import os
import numpy as np

import get_date as gd
import select_rps as sr
import new_yearly_high_price as nyhp

daily_stock_path = 'D:/pydir/Raw Data/Tushare_pro/daily_data/'
# stock_path = '/Users/pei/PycharmProjects/Raw Data/Tushare_pro/daily_data/'
report_path = 'D:/pydir/Raw Data/Report/PerReport'
# report_path = '/Users/pei/PycharmProjects/Raw Data/Report/PerReport'
result_path = 'D:/pydir/long_term/veri_result/veri_doctor_tao/'
# result_path = '/Users/pei/PycharmProjects/docter_tao/result'
weekly_stock_path = 'D:/pydir/Raw Data/Tushare_pro/weekly_data/'
# weekly_stock_path = '/Users/pei/PycharmProjects/Raw Data/Tushare_pro/weekly_data/'

start_time = time.time()

rps_N1 = 50
stock_length = 500
current_process_date = 20200327
rps_N2 = 120
rps_N3 = 250
high_price_threshold = 0.9
rps_threshold_list = [85, 85, 85]
rps_threshold_list = [80, 80, 80]

week_data_orgin = pd.read_csv(weekly_stock_path + '/000001.csv')
week_list = week_data_orgin['trade_date'].tolist()

for week_index in list(range(len(week_list)))[1:-1]:
    #获取周一的日期
    last_week_end = week_list[week_index-1]
    week_start_date = gd.get_week_start_date(last_week_end,daily_stock_path)
    #获取周五的日期
    week_end_date = week_list[week_index]
    #获取这一周每天的日期
    week_date_list = gd.get_week_date_list(week_start_date,week_end_date,daily_stock_path)
    weekly_selected_stock_list = []
    for single_date in week_date_list:
        rps_df, rps_df_above_theshold = sr.rps_sorted(daily_stock_path, rps_N1, stock_length, current_process_date)
        rps_df2, rps_df_above_theshold2 = sr.rps_sorted(daily_stock_path, rps_N2, stock_length, current_process_date)
        rps_df3, rps_df_above_theshold3 = sr.rps_sorted(daily_stock_path, rps_N3, stock_length, current_process_date)
        stock_code_df = sr.rps_reverse(daily_stock_path, rps_df_above_theshold, current_process_date)

        # 陶博士法则
        for single_code in stock_code_df['code']:
            stock_rps1 = stock_code_df[stock_code_df['code'] == single_code]['rps50'].tolist()[0]
            stock_rps2 = rps_df2[rps_df2['code'] == single_code]['rps'].tolist()[0]
            stock_rps3 = rps_df3[rps_df3['code'] == single_code]['rps'].tolist()[0]
            yearly_high_indice = nyhp.new_yearly_high_price(daily_stock_path, single_code, high_price_threshold,
                                                            current_process_date)

        #任意两线翻红
            if (stock_rps1 > rps_threshold_list[0] and stock_rps2 > rps_threshold_list[1]) or \
                    (stock_rps1 > rps_threshold_list[0] and stock_rps3 > rps_threshold_list[2]) or \
                    (stock_rps2 > rps_threshold_list[1] and stock_rps3 > rps_threshold_list[2]):
                weekly_selected_stock_list.append([single_date,single_code, stock_rps1, stock_rps2, stock_rps3,
                                                  yearly_high_indice])

    weekly_selected_stock_df = pd.DataFrame(weekly_selected_stock_list,columns=['date','code','rps1','rps2','rps3','yearly_high?'])
    weekly_selected_stock_df.to_csv(result_path + 'raw/' + str(single_date) + '.csv')

    #验证在十周线下买进
    weekly_code_list = list(set(weekly_selected_stock_df['code'].tolist()))
    for single_code in weekly_code_list:
        buy_observe_first_week = week_list[week_index+1]



'''
rps_df, rps_df_above_theshold = sr.rps_sorted(daily_stock_path, rps_N1, stock_length, current_process_date)

stock_code_df = sr.rps_reverse(stock_path, rps_df_above_theshold, current_process_date)
# 计算120,250的rps
rps_df2, rps_df_above_theshold2 = sr.rps_sorted(stock_path, rps_N2, stock_length, current_process_date)
rps_df3, rps_df_above_theshold3 = sr.rps_sorted(stock_path, rps_N3, stock_length, current_process_date)
# rps_df3_pre, rps_df_above_theshold3 = sr.rps_sorted(stock_path, rps_N3, stock_length, pre_date)
'''
