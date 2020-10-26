import pandas as pd
import math

import zeroize

daily_stock_path = 'D:/pydir/Raw Data/Tushare_pro/daily_data/'
# stock_path = '/Users/pei/PycharmProjects/Raw Data/Tushare_pro/daily_data/'
report_path = 'D:/pydir/Raw Data/Report/PerReport'
# report_path = '/Users/pei/PycharmProjects/Raw Data/Report/PerReport'
result_path = 'D:/pydir/long_term/veri_result/veri_doctor_tao/'
# result_path = '/Users/pei/PycharmProjects/docter_tao/result'
weekly_stock_path = 'D:/pydir/Raw Data/Tushare_pro/weekly_data/'
# weekly_stock_path = '/Users/pei/PycharmProjects/Raw Data/Tushare_pro/weekly_data/'

rps_threshold_list = [70, 70, 70]
result_path = result_path + str(rps_threshold_list[0]) + '/'

buy_date_log = pd.read_csv(result_path + 'buy_stock_log.csv')
#现在的buy_date_log中buy_date是float型，需要转为整型，同时，诸如1的股票代码也需要转为000001
stock_code_list = []
buy_date_list = []
for index in range(len(buy_date_log)):
    stock_code_list.append(zeroize.zeroize(buy_date_log['stock_code'].tolist()[index]))
    if math.isnan(buy_date_log['buy_date'].tolist()[index]) == False:
        buy_date_list.append(str(int(buy_date_log['buy_date'].tolist()[index])))
    else:
        buy_date_list.append(buy_date_log['buy_date'].tolist()[index])

buy_date_log.drop(['stock_code','buy_date'],axis=1)
buy_date_log['stock_code'] = stock_code_list
buy_date_log['buy_date'] = buy_date_list


