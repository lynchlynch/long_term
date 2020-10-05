import os
import pandas as pd

finance_data_path = 'D:/pydir/Raw Data/Tushare_pro/finance_data/'

file_list = os.listdir(finance_data_path)

for single_file in file_list:
    stock_data = pd.read_csv(finance_data_path + single_file)
    eps_yoy_list = stock_data['basic_eps_yoy'].tolist()
    eps_current = eps_yoy_list[0]
    eps_pre_1 = eps_yoy_list[1]
    eps_pre_2 = eps_yoy_list[2]