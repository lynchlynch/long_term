#由于Tushare数据放在私人服务器中，如果一次获取较多数据，容易被误认为是DDos攻击，故分组获取
import tushare as ts
import time
import pandas as pd
import os
from tqdm import tqdm

ts.set_token('d34c57b1749de7df7766a60bb615078696e935856d99575c6b91bb5d')
pro = ts.pro_api('d34c57b1749de7df7766a60bb615078696e935856d99575c6b91bb5d')
stock_code = pro.stock_basic(exchange='', list_status='L', fields='ts_code')['ts_code']
leap = 5#设置每组股票数
groups = list(range(0,len(stock_code)//leap + 1))#分组
no_data_stocks = []#储存无数据股票代码，以便重新下载
download_failed_stocks = []
# root_path = '/Users/pei/PycharmProjects/Raw Data/Tushare_pro/weekly_data/'
root_path = 'D:/pydir/Raw Data/Tushare_pro/weekly_data/'

# start_date = '20171009'
start_date = '20111009'
current_day = '20200424'

start_time = time.time()

#分组下载数据
for group in tqdm(groups,desc='group'):
    for stock_code_index in stock_code[(group-1) * leap : group * leap -1]:
        try:
            single_stock_data = ts.pro_bar\
                (ts_code=stock_code_index, adj='qfq', start_date=start_date,end_date=current_day,
                 ma=[5, 10, 20, 30, 50, 60, 120, 250],freq='W')
            single_stock_data.sort_values(by='trade_date',axis = 0, ascending = True,inplace=True)
            single_stock_data = single_stock_data.reset_index(drop=True)
            # print(single_stock_data)
            single_stock_savepath = root_path + stock_code_index.split('.')[0] + '.csv'
            single_stock_data.to_csv(single_stock_savepath)

        except AttributeError:
            download_failed_stocks.append(stock_code_index)

#下载未进入分组的最后几只股票
for i in tqdm(stock_code[-leap:],desc='undownload stocks'):
    try:
        single_stock_data = ts.pro_bar \
            (ts_code=stock_code_index, adj='qfq', start_date=start_date,
             end_date=current_day, ma=[5, 10, 20, 30, 50, 60, 120])
        single_stock_data.sort_values(by='trade_date', axis=0, ascending=True, inplace=True)
        single_stock_data = single_stock_data.reset_index(drop=True)
        single_stock_savepath = root_path + stock_code_index + '.csv'
        single_stock_data.to_csv(single_stock_savepath)
    except AttributeError:
        download_failed_stocks.append(i)

re_try_nums = 5#重试次数
#重新下载
re_try_list = list(range(0,re_try_nums))
for re_try_num in tqdm(re_try_list,desc='re_try'):
    for no_data_stock in download_failed_stocks:
        try:
            print(no_data_stock)
            single_stock_data = ts.pro_bar\
                (ts_code=stock_code_index, adj='qfq', start_date=start_date,
                 end_date=current_day, ma=[5, 10, 20, 30, 50, 60, 120],freq='W')
            single_stock_savepath = root_path + stock_code_index.split('.')[0] + '.csv'
            single_stock_data.to_csv(single_stock_savepath)
            download_failed_stocks.remove(no_data_stock)
        except AttributeError:
            pass

print('The following stock is failed to downloaded:\n')
#储存下载失败股票代码
for download_failed_stock in tqdm(download_failed_stocks,desc='save failed downloads'):
    with open(root_path + 'downloaden_failed_stocks.txt', 'a') as file_object:
        file_object.write(download_failed_stock)
        file_object.write('\n')
#储存无数据股票
for no_data_stock in tqdm(no_data_stocks,'save the no_data_stock'):
    with open(root_path + 'no_data_stock.txt', 'a') as file_object:
        file_object.write(no_data_stock)
        file_object.write('\n')


end_time = time.time()

print(end_time - start_time)