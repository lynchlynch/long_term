import time
import pandas as pd
from multiprocessing import Pool
import os
import numpy as np
import time

import get_date as gd
import select_rps as sr
import new_yearly_high_price as nyhp
import zeroize

start_time = time.time()

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
# current_process_date = 20200306
rps_N2 = 120
rps_N3 = 250
high_price_threshold = 0.9
rps_threshold_list = [80, 80, 80]
# rps_threshold_list = [80, 80, 80]
result_path = result_path + str(rps_threshold_list[0]) + '/'

duration_month = 8
duration_day = duration_month * 4 * 5
target_rate = 0.5

week_data_orgin = pd.read_csv(weekly_stock_path + '/000001.csv')
week_list = week_data_orgin['trade_date'].tolist()
# print(len(week_list))

#获取周线文件列表
weekly_file_list = os.listdir(weekly_stock_path)
for single_file in weekly_file_list:
    if single_file.split('.')[1] != 'csv':
        os.remove(weekly_stock_path + single_file)
weekly_file_list = os.listdir(weekly_stock_path)

# for week_index in list(range(len(week_list)))[-1:]:
for week_index in list(range(len(week_list)))[52:275]:
    #获取周一的日期
    last_week_end = week_list[week_index-1]
    week_start_date = gd.get_week_start_date(last_week_end,daily_stock_path)
    #获取周五的日期
    week_end_date = week_list[week_index]
    #获取这一周每天的日期
    week_date_list = gd.get_week_date_list(week_start_date,week_end_date,daily_stock_path)
    weekly_selected_stock_list = []
    for single_date in week_date_list:
        total_stock_list = []
        current_process_date = single_date
        print('current_process_date ： ' + str(current_process_date))
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
                if (single_code + '.csv') in weekly_file_list:
                    weekly_selected_stock_list.append([single_date,single_code, stock_rps1, stock_rps2, stock_rps3,
                                                      yearly_high_indice])

    weekly_selected_stock_df = pd.DataFrame(weekly_selected_stock_list,columns=['date','code','rps1','rps2','rps3','yearly_high?'])
    weekly_selected_stock_df.to_csv(result_path + 'raw/' + str(single_date) + '.csv')

    #验证在十周线下买进
    weekly_code_list = list(set(weekly_selected_stock_df['code'].tolist()))
    for single_code in weekly_code_list:
        print(single_code)
        # print(week_end_date)
        single_stock_data = pd.read_csv(daily_stock_path + zeroize.zeroize(single_code) + '.csv')
        single_stock_week_data = pd.read_csv(weekly_stock_path + single_code + '.csv')
        buy_observe_first_week = gd.get_first_observe_date(single_stock_data,week_end_date)
        # print(buy_observe_first_week)
        if type(buy_observe_first_week) == int:
            buy_date_monday = gd.get_buy_date_10(single_stock_data,single_stock_week_data,buy_observe_first_week)
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
                if len([single_code,buy_date_monday,sell_date,sell_date_index-buy_date_index_daily,
                                         buy_price,highest_price,increase_rate]) != 0:
                    total_stock_list.append([single_code,buy_date_monday,sell_date,sell_date_index-buy_date_index_daily,
                                            buy_price,highest_price,increase_rate])

    total_stock_df = pd.DataFrame(total_stock_list,columns=['code','buy_date','sell_date','duration(day)',
                                                            'buy_price','sell_price','increase_rate'])
    total_stock_df.to_csv(result_path + 'buy_under_10k/' + str(week_end_date) + '.csv',index=False)

per_day_result_list = os.listdir(result_path + 'buy_under_10k/')
for single_file in per_day_result_list:
    if single_file.split('.')[1] != 'csv':
        os.remove(result_path + 'buy_under_10k/' + single_file)
per_day_result_list = os.listdir(result_path + 'buy_under_10k/')

weigh = list(round(i,2) for i in list(0.1 * np.array(range(-10,11))))#为了统计各个上涨率的比例
statistic_list = list(np.zeros(len(weigh)))
count_num = 0
total_num = 0

#由于有可能存在连续好几天都出现doctor tao信号，而他们都是统一在同一天购买，因此会出现重复统计的情况，
# 因此记录一下买入时间，以便去重
buy_stock_log = []

for single_file in per_day_result_list:
    single_file_data = pd.read_csv(result_path + 'buy_under_10k/' + single_file)
    for code_index in range(len(single_file_data)):
        stock_code = single_file_data['code'].tolist()[code_index]
        buy_date = single_file_data['buy_date'].tolist()[code_index]
        if [stock_code,buy_date] not in buy_stock_log:
            buy_stock_log.append([stock_code,buy_date])
            total_num += 1
            increase_rate = single_file_data['increase_rate'].tolist()[code_index]
            # 计算涨跌区间
            if increase_rate >= 1:
                statistic_list[-1] += 1
            elif increase_rate <= -1:
                statistic_list[0] += 1
            else:
                for weigh_index in range(1, len(weigh) - 2):
                    if (increase_rate - weigh[weigh_index]) * (increase_rate - weigh[weigh_index + 1]) <= 0:
                        statistic_list[weigh_index] += 1
                        break
            #计算满足上涨条件的数量
            if increase_rate >= target_rate:
                count_num += 1
    if len(single_file_data) == 0:
        os.remove(result_path + 'buy_under_10k/' + single_file)

print(count_num/total_num)


end_time = time.time()
print('time elapse : ' + str(end_time-start_time))
