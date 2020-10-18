#验证在十周线下买进
import time
import pandas as pd
from multiprocessing import Pool
import os
import numpy as np
import time

import zeroize
import get_date as gd

daily_stock_path = 'D:/pydir/Raw Data/Tushare_pro/daily_data/'
# stock_path = '/Users/pei/PycharmProjects/Raw Data/Tushare_pro/daily_data/'
report_path = 'D:/pydir/Raw Data/Report/PerReport'
# report_path = '/Users/pei/PycharmProjects/Raw Data/Report/PerReport'
result_path = 'D:/pydir/long_term/veri_result/veri_doctor_tao/'
# result_path = '/Users/pei/PycharmProjects/docter_tao/result'
weekly_stock_path = 'D:/pydir/Raw Data/Tushare_pro/weekly_data/'
# weekly_stock_path = '/Users/pei/PycharmProjects/Raw Data/Tushare_pro/weekly_data/'

duration_month = 8
duration_day = duration_month * 4 * 5
rps_threshold_list = [80, 80, 80]
result_path = result_path + str(rps_threshold_list[0]) + '/'
single_date = 20131101
week_end_date = 20131101

weekly_selected_stock_df = pd.read_csv(result_path + 'raw/' + str(single_date) + '.csv')

weekly_code_list = list(set(weekly_selected_stock_df['code'].tolist()))
total_stock_list = []
for single_code in weekly_code_list:
    # print(type(single_code))
    # single_code = str(single_code)
    # single_stock_file = daily_stock_path + zeroize.zeroize(single_code) + '.csv'
    single_stock_data = pd.read_csv(daily_stock_path + zeroize.zeroize(single_code) + '.csv')
    single_stock_week_data = pd.read_csv(weekly_stock_path + zeroize.zeroize(single_code) + '.csv')
    buy_observe_first_week = gd.get_first_observe_date(single_stock_data,week_end_date)
    print(buy_observe_first_week)
    if type(buy_observe_first_week) == int:
        buy_date_monday = gd.get_buy_date_10(single_stock_data,single_stock_week_data,buy_observe_first_week)
        print(buy_date_monday)
        if (type(buy_date_monday)) == int:# and ([single_code,buy_date_monday] in buy_stock_log):
            #由于有可能存在连续好几天都出现doctor tao信号，而他们都是统一在同一天购买，因此会出现重复统计的情况，
            # 因此记录一下买入时间，以便去重
            buy_date_index_daily = single_stock_data['trade_date'].tolist().index(buy_date_monday)
            buy_price = single_stock_data['high'].tolist()[buy_date_index_daily]#用最高价测试
            if (buy_date_index_daily + duration_day) <= len(single_stock_data):
                highest_price = max(single_stock_data['high'].tolist()
                                    [buy_date_index_daily:(buy_date_index_daily + duration_day)])
                print(duration_day)
                print(highest_price)
                sell_date_index = single_stock_data['high'].tolist()[
                                  buy_date_index_daily:(buy_date_index_daily + duration_day)].index(highest_price) + \
                                  buy_date_index_daily
                print(buy_date_index_daily)
                print(sell_date_index)
                sell_date = single_stock_data['trade_date'].tolist()[sell_date_index]
            else:
                highest_price = max(single_stock_data['high'].tolist()
                                    [buy_date_index_daily:len(single_stock_data)])
                sell_date_index = single_stock_data['high'].tolist()[
                                  buy_date_index_daily:len(single_stock_data)].index(highest_price) + \
                                  buy_date_index_daily
                # print(buy_date_index_daily)
                # print(sell_date_index)
                sell_date = single_stock_data['trade_date'].tolist()[sell_date_index]
            increase_rate = (highest_price - buy_price) / buy_price
            '''
            if len([single_code,buy_date_monday,sell_date,sell_date_index-buy_date_index_daily,
                                     buy_price,highest_price,increase_rate]) != 0:
                total_stock_list.append([single_code,buy_date_monday,sell_date,sell_date_index-buy_date_index_daily,
                                        buy_price,highest_price,increase_rate])
            '''

    total_stock_list.append([single_code, buy_date_monday, sell_date, sell_date_index - buy_date_index_daily,
                         buy_price, highest_price, increase_rate])
total_stock_df = pd.DataFrame(total_stock_list,columns=['code','buy_date','sell_date','duration(day)',
                                                        'buy_price','sell_price','increase_rate'])
total_stock_df.to_csv(result_path + 'buy_under_10k/' + str(week_end_date) + '.csv',index=False)