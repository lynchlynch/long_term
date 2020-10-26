import os
import pandas as pd
import numpy as np

# finance_data_path = 'D:/pydir/Raw Data/Tushare_pro/finance_data/'
def C_rule(finance_data_path,stock_code):
    file_list = os.listdir(finance_data_path)

    # for single_file in file_list:
    print('--------------'+stock_code+'----------------')
    stock_data = pd.read_csv(finance_data_path + stock_code + '.csv')
    eps_yoy_list = stock_data['basic_eps_yoy'].tolist()
    eps_current = eps_yoy_list[0]
    eps_pre_1 = eps_yoy_list[1]
    eps_pre_2 = eps_yoy_list[2]
    eps_pre_3 = eps_yoy_list[3]

    diff_eps_current = eps_current - eps_pre_1
    diff_eps_1 = eps_pre_1 - eps_pre_2
    diff_eps_2 = eps_pre_2 - eps_pre_3

    if (eps_current > 0.4) and (diff_eps_current - diff_eps_1) > 0 and (diff_eps_1-diff_eps_2) > 0:
        satisfy_c_rule = True

