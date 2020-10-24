import time
import pandas as pd
from multiprocessing import Pool
import os
import numpy as np
import time
from numba import jit

import get_date as gd
import select_rps as sr
import new_yearly_high_price as nyhp
import zeroize
import test_buy_date as tbd

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
# current_process_date = 202001007
rps_N2 = 120
rps_N3 = 250
high_price_threshold = 0.9
# rps_threshold_list = [85, 85, 85]
rps_threshold_list = [80, 80,  80]
result_path = result_path + str(rps_threshold_list[0]) + '/'

duration_month = 8
duration_day = duration_month * 4 * 5
target_rate = 0.5

week_data_orgin = pd.read_csv(weekly_stock_path + '/000001.csv')
week_list = week_data_orgin['trade_date'].tolist()

#获取周线文件列表
weekly_file_list = os.listdir(weekly_stock_path)
for single_file in weekly_file_list:
    if single_file.split('.')[1] != 'csv':
        os.remove(weekly_stock_path + single_file)
weekly_file_list = os.listdir(weekly_stock_path)
# print(week_list.index(20141219))
# p = Pool(processes=10)
for week_index in list(range(len(week_list)))[52:]:
    # print(week_list[week_index])
    tbd.get_per_stock_buy_date(week_list,week_index,daily_stock_path,weekly_stock_path,result_path,rps_N1,rps_N2,rps_N3,
                           stock_length,high_price_threshold,rps_threshold_list,weekly_file_list,duration_day)
    # p.apply_async(get_per_stock_buy_date,args=(week_list,week_index,daily_stock_path,weekly_stock_path,
    #                                            result_path,rps_N1,rps_N2,rps_N3,stock_length,
#                                                high_price_threshold,rps_threshold_list,weekly_file_list))
# p.close()
# p.join()

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

print(count_num/total_num)

buy_stock_log_df = pd.DataFrame(buy_stock_log, columns=['stock_code', 'buy_date'])
buy_stock_log_df.to_csv(result_path + 'buy_stock_log.csv')

end_time = time.time()
print('time elapse : ' + str(end_time-start_time))