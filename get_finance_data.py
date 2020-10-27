import tushare as ts
import time
from tqdm import tqdm

ts.set_token('d34c57b1749de7df7766a60bb615078696e935856d99575c6b91bb5d')
pro = ts.pro_api('d34c57b1749de7df7766a60bb615078696e935856d99575c6b91bb5d')
stock_code = pro.stock_basic(exchange='', list_status='L', fields='ts_code')['ts_code']

leap = 5#设置每组股票数
groups = list(range(0,len(stock_code)//leap + 1))#分组
no_data_stocks = []#储存无数据股票代码，以便重新下载
download_failed_stocks = []
root_path = '/Users/pei/PycharmProjects/Raw Data/Tushare_pro/daily_data/'
# root_path = 'D:/pydir/Raw Data/Tushare_pro/finance_data/'

# start_date = '20171009'
start_date = '20121009'
current_day = '20201026'

start_time = time.time()

for single_code in tqdm(stock_code,desc='downloading'):
    df = pro.fina_indicator(ts_code = single_code,start_date = start_time,end_date = current_day)
    time.sleep(0.6)#每分钟最多访问80次，所以只能睡眠
    df.to_csv(root_path + single_code.split('.')[0] + '.csv',index= False)
