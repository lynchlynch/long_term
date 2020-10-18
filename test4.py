import os
import numpy as np
import pandas as pd

result_path = 'D:/pydir/long_term/veri_result/veri_doctor_tao/'
rps_threshold_list = [80, 80, 80]
result_path = result_path + str(rps_threshold_list[0]) + '/'
target_rate = 0.5

per_day_result_list = os.listdir(result_path + 'buy_under_10k/')
for single_file in per_day_result_list:
    if single_file.split('.')[1] != 'csv':
        os.remove(result_path + 'buy_under_10k/' + single_file)
per_day_result_list = os.listdir(result_path + 'buy_under_10k/')
print(len(per_day_result_list))

weigh = list(round(i,2) for i in list(0.1 * np.array(range(-10,11))))#为了统计各个上涨率的比例
statistic_list = list(np.zeros(len(weigh)))
count_num = 0
total_num = 0

#由于有可能存在连续好几天都出现doctor tao信号，而他们都是统一在同一天购买，因此会出现重复统计的情况，
# 因此记录一下买入时间，以便去重
buy_stock_log = []

for single_file in per_day_result_list:
    single_file_data = pd.read_csv(result_path + 'buy_under_10k/' + single_file)
    for code_index in range(len(single_file_data)):
        stock_code = single_file_data['code'].tolist()[code_index]
        buy_date = single_file_data['buy_date'].tolist()[code_index]
        if [stock_code, buy_date] not in buy_stock_log:
            buy_stock_log.append([stock_code, buy_date])
            total_num += 1
            increase_rate = single_file_data['increase_rate'].tolist()[code_index]
            # 计算涨跌区间
            if increase_rate >= 1:
                statistic_list[-1] += 1
            elif increase_rate <= -1:
                statistic_list[0] += 1
            else:
                for weigh_index in range(1, len(weigh) - 2):
                    if (increase_rate - weigh[weigh_index]) * (increase_rate - weigh[weigh_index + 1]) <= 0:
                        statistic_list[weigh_index] += 1
                        break
            # 计算满足上涨条件的数量
            if increase_rate >= target_rate:
                count_num += 1

print(count_num / total_num)

buy_stock_log_df = pd.DataFrame(buy_stock_log, columns=['stock_code', 'buy_date'])
buy_stock_log_df.to_csv(result_path + 'buy_stock_log.csv')