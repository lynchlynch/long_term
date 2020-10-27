import pandas as pd
import os

# import

def C_rule(finance_data_path,stock_code):
    disclosure_result_path = 'D:/pydir/Raw Data/Tushare_pro/disclosure_date/'
    disclosure_result_data = pd.read_csv(disclosure_result_path + 'total_disclosure.csv')
    # report_date = disclosure_result_data[(disclosure_result_data['stock_code'] == int(stock_code)) and ]
    # print('--------------'+stock_code+'----------------')
    if os.path.exists(finance_data_path + stock_code + '.csv'):
        stock_data = pd.read_csv(finance_data_path + stock_code + '.csv')
        print(stock_data)
        eps_yoy_list = stock_data['basic_eps_yoy'].tolist()
        eps_current = eps_yoy_list[0]
        eps_pre_1 = eps_yoy_list[1]
        eps_pre_2 = eps_yoy_list[2]
        eps_pre_3 = eps_yoy_list[3]

        diff_eps_current = eps_current - eps_pre_1
        diff_eps_1 = eps_pre_1 - eps_pre_2
        diff_eps_2 = eps_pre_2 - eps_pre_3

        if (eps_current > 0.4) and (diff_eps_current - diff_eps_1) > 0 and (diff_eps_1-diff_eps_2) > 0:
            satisfy_c_rule = 'True'
            print('True')
        else:
            satisfy_c_rule = 'False'
    else:
        satisfy_c_rule = 'N'

    return satisfy_c_rule

