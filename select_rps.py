import pandas as pd
import os
import time
import datetime

import count_within_period as cwp

def single_increase_rate(stock_data,rps_N,rps_index):#single_stock的长度必须大于rps_N
    ref_price = stock_data['close'][rps_index-rps_N]
    current_price = stock_data['close'][rps_index]
    increase_rate = (current_price-ref_price)/ref_price * 1000#放大1000倍
    return current_price,increase_rate
    # print(increase_rate)

def derive_date():
    now_time = datetime.datetime.now()
    year = str(now_time.year)
    if now_time.month < 10:
        month = '0' + str(now_time.month)
    else:
        month = str(now_time.month)
    if now_time.day < 10:
        day = '0' + str(now_time.day)
    else:
        day =  str(now_time.day)
    return year + '-' + month + '-' + day

#返回股票代码及rps
def rps_sorted(stock_path,rps_N,stock_length,current_process_date):
    start_time = time.time()
    #删除不是csv的文件
    file_list = os.listdir(stock_path)
    for single_file in file_list:
        if single_file.split('.')[1] != 'csv':
            os.remove(stock_path + '/' + single_file)

    file_list = os.listdir(stock_path)
    increase_rate_list = []#[stock[code,date,rps,close]]
    initial_value = -3000#若当天无数据，则将增长率置为-3000
    for single_stock in file_list:
        # print(single_stock)
        stock_data = pd.read_csv(stock_path + '/' + single_stock)
        if len(stock_data) > stock_length:
            # if str(stock_data['date'][len(stock_data)-1]) == current_process_date:
            if len(stock_data[stock_data['trade_date'] == current_process_date]) != 0:
                rps_index = stock_data[stock_data['trade_date']==current_process_date].index.values[0]
                if rps_index >= rps_N:
                    current_price, increase_rate = single_increase_rate(stock_data, rps_N, rps_index)
                    single_code = single_stock.split('.')[0]
                    increase_rate_list.append([single_code, current_price, increase_rate])

    rps_df = pd.DataFrame(increase_rate_list, columns=['code', 'current_price', 'increase_rate'])
    rps_df.sort_values(by='increase_rate', axis=0, ascending=False, inplace=True)
    rps_list = []
    stock_total_num = len(rps_df)
    for df_index in range(len(rps_df)):
        single_rps = round((1 - df_index / stock_total_num) * 100, 3)
        rps_list.append(single_rps)
    rps_df['rps'] = rps_list
    rps_df_above_theshold = rps_df[rps_df['rps'] >= 85]
    return rps_df,rps_df_above_theshold

#月线反转5.0，来源：陶博士2006公众号

def rps_reverse(stock_path,rps_df_above_theshold,current_process_date):
    stock_code_list = []#储存最终选出来的股票代码
    for single_code in list(rps_df_above_theshold['code']):
        # print(single_code)
        stock_data = pd.read_csv(stock_path + '/' + single_code + '.csv')
        index = stock_data[stock_data['trade_date'] == current_process_date].index.values[0]
        #日线收盘价站上年线
        ma_250_list = stock_data['ma250']
        above_line = stock_data['close'][index] > ma_250_list[index]
        # print(above_line)
        #一个月内曾创50日新高
        highest_list = stock_data['high'][index-50+1:index+1]
        highest_within_50 = max(highest_list)
        highest_within_period_30 = \
            cwp.count_within_period(highest_list, index, highest_within_50, 30, 0)
        # print(highest_within_period_30)
        #收盘价站上年线的天数大于2，小于30
        close_satisfied_yearly = 0
        for i in range(index-30+1,index+1):
            if stock_data['close'][i] >= ma_250_list[i]:
                close_satisfied_yearly += 1
        # print(close_satisfied_yearly)
        #最高价距离120日内的最高价不到10%
        today_high = stock_data['high'][index]
        if index >= 120:
            highest_120 = max(stock_data['high'][index-120+1:index+1])
            highest_to_120 = today_high/highest_120 >=0.9
        else:
            continue
        # print(highest_to_120)
        # print('------------------------')

        if (above_line == True) and (highest_within_period_30 >= 1) and \
                (close_satisfied_yearly > 2) and (close_satisfied_yearly < 30) and \
                (highest_to_120 == True):
            stock_rps_50 = rps_df_above_theshold[rps_df_above_theshold['code']==single_code]['rps'].tolist()[0]
            stock_code_list.append([single_code,stock_rps_50])

    stock_code_df = pd.DataFrame(stock_code_list,columns=['code','rps50'])
    return stock_code_df