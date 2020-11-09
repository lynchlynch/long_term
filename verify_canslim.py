import pandas as pd
import os
import math
from tqdm import tqdm

import zeroize
import C_rule
import A_rule

# daily_stock_path = 'D:/pydir/Raw Data/Tushare_pro/daily_data/'
stock_path = '/Users/pei/PycharmProjects/Raw Data/Tushare_pro/daily_data/'
# report_path = 'D:/pydir/Raw Data/Report/PerReport'
report_path = '/Users/pei/PycharmProjects/Raw Data/Report/PerReport'
# result_path = 'D:/pydir/long_term/veri_result/veri_doctor_tao/'
result_path = '/Users/pei/long_term/veri_result/veri_doctor_tao'
# weekly_stock_path = 'D:/pydir/Raw Data/Tushare_pro/weekly_data/'
weekly_stock_path = '/Users/pei/PycharmProjects/Raw Data/Tushare_pro/weekly_data/'
# finance_data_path = 'D:/pydir/Raw Data/Tushare_pro/finance_data/'

duration_month = 8
duration_day = duration_month * 4 * 5
target_rate = 0.5

rps_threshold_list = [95, 95, 95]
result_path = result_path + str(rps_threshold_list[0]) + '/'

buy_date_log = pd.read_csv(result_path + 'buy_stock_log.csv')
#现在的buy_date_log中buy_date是float型，需要转为整型，同时，诸如1的股票代码也需要转为000001
c_rule_list = []
a_rule_list = []
canslim_verify_df = pd.DataFrame([],columns=['stock_code','buy_date'])

if os.path.exists(result_path + 'canslim_verify_result.csv') == False:
    for index in tqdm(range(len(buy_date_log))[:100],desc='processing'):
    # for index in range(len(buy_date_log)):
        # print('--------------' +str(index) + '-------------------------')
        if math.isnan(buy_date_log['buy_date'].tolist()[index]) == False:
            new_stock_code = zeroize.zeroize(buy_date_log['stock_code'].tolist()[index])
            new_buy_date = str(int(buy_date_log['buy_date'].tolist()[index]))
            canslim_verify_df = canslim_verify_df.append([{'stock_code':new_stock_code,'buy_date':new_buy_date}])
            ############# C Rule###########################
            c_rule_result = C_rule.C_rule(finance_data_path,new_stock_code,new_buy_date)
            c_rule_list.append(c_rule_result)

            ############# A Rule###########################
            a_rule_result = A_rule.A_rule(finance_data_path, new_stock_code, new_buy_date)
            a_rule_list.append(c_rule_result)
            # if c_rule_result == 'True':
            #     print(c_rule_result)
            #     true_num = true_num+1
    # print(true_num/len(c_rule_list))
    '''
        stock_code_list.append(zeroize.zeroize(buy_date_log['stock_code'].tolist()[index]))
        if math.isnan(buy_date_log['buy_date'].tolist()[index]) == False:
            buy_date_list.append(str(int(buy_date_log['buy_date'].tolist()[index])))
        else:
            buy_date_list.append(buy_date_log['buy_date'].tolist()[index])
        
    
    buy_date_log.drop(['stock_code','buy_date'],axis=1)
    buy_date_log['stock_code'] = stock_code_list
    buy_date_log['buy_date'] = buy_date_list
    '''
    canslim_verify_df['C_rule'] = c_rule_list
    canslim_verify_df['A_rule'] = a_rule_list
    canslim_verify_df = canslim_verify_df.reset_index(drop=True)
    canslim_verify_df.to_csv(result_path + 'canslim_verify_result.csv')

canslim_verify_df = pd.read_csv(result_path + 'canslim_verify_result.csv')
satisfy_c_a_df = canslim_verify_df[(canslim_verify_df['C_rule'] == 'True') & (canslim_verify_df['A_rule'] == 'True')]
print(len(satisfy_c_a_df))
satisfy_num = 0

satisfy_canslim_df = pd.DataFrame([])

for index in range(len(satisfy_c_a_df)):
    stock_code = satisfy_c_a_df['stock_code'].tolist()[index]
    buy_date = satisfy_c_a_df['buy_date'].tolist()[index]
    # print(str(stock_code) + '-------' + str(buy_date))
    # print(zeroize.zeroize(stock_code))
    stock_data = pd.read_csv(daily_stock_path + zeroize.zeroize(stock_code) + '.csv')
    buy_date_index = stock_data['trade_date'].tolist().index(buy_date)
    buy_price = stock_data['high'].tolist()[buy_date_index]
    # print(str(stock_code) + '-------' + str(buy_date) + '-----------' + str(buy_date_index + duration_day+1) +
    #       '-----------' + str(len(stock_data)))
    if (buy_date_index + duration_day+1) < len(stock_data):
        high_price = max(stock_data['high'].tolist()[buy_date_index+1:buy_date_index+duration_day+1])
        # print(str(stock_code) + '-------' + str(buy_date) + '-----------' + str(high_price))
    else:
        high_price = max(stock_data['high'].tolist()[buy_date_index + 1:])

    increase_rate = (high_price - buy_price) / buy_price
    print(increase_rate)
    if increase_rate > 0.5:
        satisfy_num += 1
        # satisfy_canslim_df = satisfy_canslim_df.append([{'stock_code':zeroize.zeroize(stock_code),'buy_date':buy_date,
        #                                                  'increase':increase_rate}])

satisfy_canslim_df.to_csv(result_path + 'satisfy_canslim.csv')
print('satisfy_rate = ' + str(satisfy_num/len(satisfy_c_a_df)))


