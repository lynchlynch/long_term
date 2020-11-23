import pandas as pd
import draw_k_line_fuc
import zeroize
import time
from tqdm import tqdm

start_time = time.time()

# daily_stock_path = 'D:/pydir/Raw Data/Tushare_pro/daily_data/'
daily_stock_path = '/Users/pei/PycharmProjects/Raw Data/Tushare_pro/daily_data/'
# weekly_stock_path = 'D:/pydir/Raw Data/Tushare_pro/weekly_data/'
weekly_stock_path = '/Users/pei/PycharmProjects/Raw Data/Tushare_pro/weekly_data/'
# monthly_stock_path = 'D:/pydir/Raw Data/Tushare_pro/monthly_data/'
monthly_stock_path = '/Users/pei/PycharmProjects/Raw Data/Tushare_pro/monthly_data/'
# report_path = 'D:/pydir/Raw Data/Report/PerReport'
report_path = '/Users/pei/PycharmProjects/Raw Data/Report/PerReport'
# result_path = 'D:/pydir/long_term/veri_result/veri_doctor_tao/'
result_path = '/Users/pei/PycharmProjects/long_term/veri_result/veri_doctor_tao/'
# weekly_stock_path = 'D:/pydir/Raw Data/Tushare_pro/weekly_data/'
weekly_stock_path = '/Users/pei/PycharmProjects/Raw Data/Tushare_pro/weekly_data/'

rps = 85
period_pre_daily = 500
period_post_daily = 250
period_pre_weekly = 100
period_post_weekly = 50
period_pre_monthly = 25
period_post_monthly = 13
result_path = result_path + str(rps) + '/'
to_draw_file = 'buy_stock_log.csv'

to_draw_file_df = pd.read_csv(result_path + to_draw_file)
to_draw_file_df = to_draw_file_df.dropna()
to_draw_file_df = to_draw_file_df.drop('Unnamed: 0',axis=1)

# for index in range(len(to_draw_file_df)):
for index in tqdm(range(len(to_draw_file_df)),desc='index'):
    single_stock_code = to_draw_file_df['stock_code'].tolist()[index]
    single_stock_code = zeroize.zeroize(single_stock_code)
    single_buy_date = int(to_draw_file_df['buy_date'].tolist()[index])
    ##画日K线
    draw_k_line_fuc.draw_k_line(daily_stock_path,result_path + 'raw_tao/daily/',single_stock_code,
                                single_buy_date,period_pre_daily,period_post_daily)
    # ##画周K线
    # draw_k_line_fuc.draw_k_line(weekly_stock_path, result_path + 'raw_tao/weekly/', single_stock_code,
    #                             single_buy_date, period_pre_weekly, period_post_weekly)


end_time = time.time()
print(end_time - start_time)