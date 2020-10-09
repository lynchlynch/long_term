import tushare as ts
import os
import pandas as pd

disclosure_result_path = 'D:/pydir/Raw Data/Tushare_pro/disclosure_date/'

ts.set_token('d34c57b1749de7df7766a60bb615078696e935856d99575c6b91bb5d')
pro = ts.pro_api('d34c57b1749de7df7766a60bb615078696e935856d99575c6b91bb5d')

year_list = list(range(2011,2021))
year_list = [str(i) for i in year_list]
end_quater_list = ['0331','0630','0930','1231']
for single_year in year_list:
    for single_quater in end_quater_list:
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

total_disclosure_df.to_csv(disclosure_result_path + 'total_disclosure.csv',index=False)