import pandas as pd
import numpy as np
import os
import time
import matplotlib as plt

start_time = time.time()

weekly_stock_path = '/Users/pei/PycharmProjects/Raw Data/Tushare_pro/weekly_data/'
daily_stock_path = '/Users/pei/PycharmProjects/Raw Data/Tushare_pro/daily_data/'
result_root_path = '/Users/pei/PycharmProjects/long_term/'

file_list = os.listdir(weekly_stock_path)
process_file_list = []#储存有50周以上数据的股票文件列表，实际上只处理30周的
duration = 32#统计8个月内的涨幅
total_num = 0
count_num = 0
target_rate = 0.5
weigh = list(round(i,2) for i in list(0.1 * np.array(range(-10,11))))#为了统计各个上涨率的比例
statistic_list = list(np.zeros(len(weigh)))

for single_file in file_list:
    if single_file.split('.')[1] != 'csv':
        os.remove(weekly_stock_path + single_file)
    else:
        stock_data = pd.read_csv(weekly_stock_path + single_file)
        if len(stock_data) > 50:
            process_file_list.append(single_file)

for single_file in process_file_list:
    # print('------' + single_file + '------')
    stock_data = pd.read_csv(weekly_stock_path + single_file)
    selected_k_index_list = []
    lower_10k_index = []
    buy_pos_list = []#储存买点，即低于10周线后的第一周
    total_stock_list = []
    # selected_list = []
    for close_index in range(len(stock_data)-20):
        # print(stock_data['close'][close_index])
        close_price = stock_data['close'][close_index]
        close_price_post = stock_data['close'][close_index+1]
        weekly_30_k = stock_data['ma30'][close_index]
        weekly_30_k_post = stock_data['ma30'][close_index + 1]
        if close_price <= weekly_30_k and close_price_post > weekly_30_k_post:
            selected_k_index_list.append(close_index)
    for single_selected_index in range(len(selected_k_index_list)):
        #查找首次低于10周k线的位置，分两种情况，如果是最后个30周线拐点，则从它+1到最后查找；否则，只从该拐点+1到下一个拐点
        if single_selected_index < (len(selected_k_index_list)-1):#非最后一个30周线拐点
            start_pos = selected_k_index_list[single_selected_index]+1#突破30周线的下一周
            end_pos = selected_k_index_list[single_selected_index+1]
            # print('start_pos = ' + str(start_pos))
            # print('end_pos = ' + str(end_pos))
            for index in range(start_pos,end_pos):
                weekly_10_k = stock_data['ma10'][index]
                high_price = stock_data['high'][index]
                if high_price < weekly_10_k:
                    buy_pos_list.append([start_pos-1,index+1])
                    break
        else:#最后一个30周线拐点
            start_pos = selected_k_index_list[single_selected_index] + 1  # 突破30周线的下一周
            if start_pos < (len(stock_data)-1):
                for index in range(start_pos,len(stock_data)-1):
                    weekly_10_k = stock_data['ma10'][index]
                    high_price = stock_data['high'][index]
                    if high_price < weekly_10_k:
                        buy_pos_list.append([start_pos-1,index+1])
                        break
    # print(buy_pos_list)
    single_stock_increase_rate = []
    if len(buy_pos_list) != 0:
        for single_buy_pos in list(np.array(buy_pos_list)[:,1]):
            # print(single_buy_pos)
            index = list(np.array(buy_pos_list)[:,1]).index(single_buy_pos)
            buy_price = stock_data['open'][single_buy_pos]
            highest_price = max(stock_data['high'][single_buy_pos:single_buy_pos+duration+1])
            increase_rate = (highest_price - buy_price)/buy_price
            single_stock_increase_rate.append(increase_rate)
            if increase_rate > target_rate:
                count_num += 1
                # selected_list.append([stock_data['trade_date'][single_buy_pos],buy_price,highest_price,increase_rate])
                total_stock_list.append([stock_data['trade_date'][buy_pos_list[index][0]],
                                         stock_data['ma30'][buy_pos_list[index][0]],
                                         stock_data['trade_date'][single_buy_pos],buy_price,highest_price,increase_rate,1])
            else:
                total_stock_list.append([stock_data['trade_date'][buy_pos_list[index][0]],
                                         stock_data['ma30'][buy_pos_list[index][0]],
                                         stock_data['trade_date'][single_buy_pos],buy_price,highest_price,increase_rate,0])

            #计算涨跌区间
            if increase_rate >= 1:
                statistic_list[-1] += 1
            elif increase_rate <= -1:
                statistic_list[0] += 1
            else:
                for weigh_index in range(1,len(weigh)-2):
                    if (increase_rate - weigh[weigh_index]) * (increase_rate - weigh[weigh_index+1]) <= 0:
                        statistic_list[weigh_index] += 1
                        break

        total_stock_list_df = pd.DataFrame(total_stock_list,
                                           columns=['signal_date','ma30_price','buy_date','buy_price',
                                                    'highest_price','increase_rate','satisfied?'])

        total_stock_list_df.to_csv(result_root_path + 'veri_result/total/' + single_file)
        total_num += len(buy_pos_list)

print('selected rate is ' + str(count_num/total_num))
statistic_array = np.array(statistic_list)/total_num
array_used_sum = np.array([0,0,0,0,0,0,0,0,0,1,1,1,1,1,1,1,1,1,1,1,1])
print(statistic_array)

end_time = time.time()
print("time elapse : " + str(end_time-start_time))