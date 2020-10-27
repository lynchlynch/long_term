import tushare as ts
import os
import pandas as pd
from tqdm import tqdm
import numba as nba

# disclosure_result_path = 'D:/pydir/Raw Data/Tushare_pro/disclosure_date/'
disclosure_result_path = '/Users/pei/PycharmProjects/Raw Data/Tushare_pro/disclosure_date/'

ts.set_token('d34c57b1749de7df7766a60bb615078696e935856d99575c6b91bb5d')
pro = ts.pro_api('d34c57b1749de7df7766a60bb615078696e935856d99575c6b91bb5d')

year_list = list(range(2011,2021))
year_list = [str(i) for i in year_list]
end_quater_list = ['0331','0630','0930','1231']
for single_year in year_list:
    for single_quater in end_quater_list:
        # print(str(single_year) + '-----------' + str(single_quater))
        end_date = single_year + single_quater
        df = pro.disclosure_date(end_date = end_date)
        df.to_csv(disclosure_result_path + end_date + '.csv',index=False)

disclosure_file_list_raw = os.listdir(disclosure_result_path)
disclosure_file_list = []
for single_file in disclosure_file_list_raw:
    file_name = single_file.split('.')[0]
    if file_name.isdigit():
        disclosure_file_list.append(file_name + '.csv')

total_disclosure_df = pd.DataFrame([])
for single_file in disclosure_file_list:
    single_disclosure_data = pd.read_csv(disclosure_result_path + single_file)
    total_disclosure_df = total_disclosure_df.append(single_disclosure_data)

total_disclosure_df = total_disclosure_df.reset_index(drop=True)

total_disclosure_df.to_csv(disclosure_result_path + 'total_disclosure_111.csv',index=False)

code_list = []
for index in tqdm(range(len(total_disclosure_df)),desc='index'):
    code = int((total_disclosure_df['ts_code'].tolist()[index]).split('.')[0])
    code_list.append(code)
    pre_date = total_disclosure_df.loc[index,'pre_date']
    if len(str(pre_date)) < 5:#处理空值的情况
        pre_date = 0xfff

    actual_date = total_disclosure_df.loc[index, 'actual_date']
    if len(str(actual_date)) < 5:#处理空值的情况
        actual_date = 0xfff

    total_disclosure_df.loc[index,'pre_date'] = int(pre_date)
    total_disclosure_df.loc[index, 'actual_date'] = int(actual_date)
total_disclosure_df['stock_code'] = code_list
total_disclosure_df.to_csv(disclosure_result_path + 'total_disclosure.csv',index=False)