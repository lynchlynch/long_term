import pandas as pd
import math
from tqdm import tqdm

import zeroize
import C_rule

daily_stock_path = 'D:/pydir/Raw Data/Tushare_pro/daily_data/'
# stock_path = '/Users/pei/PycharmProjects/Raw Data/Tushare_pro/daily_data/'
report_path = 'D:/pydir/Raw Data/Report/PerReport'
# report_path = '/Users/pei/PycharmProjects/Raw Data/Report/PerReport'
result_path = 'D:/pydir/long_term/veri_result/veri_doctor_tao/'
# result_path = '/Users/pei/PycharmProjects/docter_tao/result'
weekly_stock_path = 'D:/pydir/Raw Data/Tushare_pro/weekly_data/'
# weekly_stock_path = '/Users/pei/PycharmProjects/Raw Data/Tushare_pro/weekly_data/'
finance_data_path = 'D:/pydir/Raw Data/Tushare_pro/finance_data/'

rps_threshold_list = [70, 70, 70]
result_path = result_path + str(rps_threshold_list[0]) + '/'

buy_date_log = pd.read_csv(result_path + 'buy_stock_log.csv')
#现在的buy_date_log中buy_date是float型，需要转为整型，同时，诸如1的股票代码也需要转为000001
c_rule_list = []
a_rule_list = []
canslim_verify_df = pd.DataFrame([],columns=['stock_code','buy_date'])
# true_num = 0
# for index in tqdm(range(len(buy_date_log))[:100],desc='processing'):
for index in range(len(buy_date_log))[:100]:
    print('--------------' +str(index) + '-------------------------')
    if math.isnan(buy_date_log['buy_date'].tolist()[index]) == False:
        new_stock_code = zeroize.zeroize(buy_date_log['stock_code'].tolist()[index])
        new_buy_date = str(int(buy_date_log['buy_date'].tolist()[index]))
        canslim_verify_df = canslim_verify_df.append([{'stock_code':new_stock_code,'buy_date':new_buy_date}])
        c_rule_result = C_rule.C_rule(finance_data_path,new_stock_code,new_buy_date)
        c_rule_list.append(c_rule_result)
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
canslim_verify_df = canslim_verify_df.reset_index(drop=True)
print(canslim_verify_df)


