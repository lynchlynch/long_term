import pandas as pd
import os

import get_date as gd
import select_rps as sr
import new_yearly_high_price as nyhp
import zeroize

def get_per_stock_buy_date(week_list,week_index,daily_stock_path,weekly_stock_path,result_path,rps_N1,
                           rps_N2,rps_N3,stock_length,high_price_threshold,rps_threshold_list,weekly_file_list,duration_day):
    last_week_end = week_list[week_index - 1]
    week_start_date = gd.get_week_start_date(last_week_end, daily_stock_path)
    # 获取周五的日期
    week_end_date = week_list[week_index]
    # print('-----------------' + str(week_end_date) + '-------------------')
    # 获取这一周每天的日期
    week_date_list = gd.get_week_date_list(week_start_date, week_end_date, daily_stock_path)
    weekly_selected_stock_list = []
    if os.path.exists(result_path + 'raw/' + str(week_date_list[-1]) + '.csv') == False:
        print('doctor tao')
        for single_date in week_date_list:
            # total_stock_list = []#10.18
            current_process_date = single_date
            print(str(week_end_date) + '-------------------' + 'current_process_date ： ' + str(current_process_date))
            rps_df, rps_df_above_theshold = sr.rps_sorted(daily_stock_path, rps_N1, stock_length, current_process_date)
            rps_df2, rps_df_above_theshold2 = sr.rps_sorted(daily_stock_path, rps_N2, stock_length, current_process_date)
            rps_df3, rps_df_above_theshold3 = sr.rps_sorted(daily_stock_path, rps_N3, stock_length, current_process_date)
            stock_code_df = sr.rps_reverse(daily_stock_path, rps_df_above_theshold, current_process_date)

            # 陶博士法则
            for single_code in stock_code_df['code']:
                stock_rps1 = stock_code_df[stock_code_df['code'] == single_code]['rps50'].tolist()[0]
                stock_rps2 = rps_df2[rps_df2['code'] == single_code]['rps'].tolist()[0]
                stock_rps3 = rps_df3[rps_df3['code'] == single_code]['rps'].tolist()[0]
                yearly_high_indice = nyhp.new_yearly_high_price(daily_stock_path, single_code, high_price_threshold,
                                                                current_process_date)

                # 任意两线翻红
                if (stock_rps1 > rps_threshold_list[0] and stock_rps2 > rps_threshold_list[1]) or \
                        (stock_rps1 > rps_threshold_list[0] and stock_rps3 > rps_threshold_list[2]) or \
                        (stock_rps2 > rps_threshold_list[1] and stock_rps3 > rps_threshold_list[2]):
                    if (single_code + '.csv') in weekly_file_list:
                        weekly_selected_stock_list.append([single_date, single_code, stock_rps1, stock_rps2, stock_rps3,
                                                           yearly_high_indice])

        weekly_selected_stock_df = pd.DataFrame(weekly_selected_stock_list,
                                                columns=['date', 'code', 'rps1', 'rps2', 'rps3', 'yearly_high?'])
        # print(result_path + 'raw/' + str(single_date) + '.csv')
        weekly_selected_stock_df.to_csv(result_path + 'raw/' + str(week_date_list[-1]) + '.csv')

    # 验证在十周线下买进
    weekly_selected_stock_df = pd.read_csv(result_path + 'raw/' + str(week_date_list[-1]) + '.csv')
    weekly_code_list = list(set(weekly_selected_stock_df['code'].tolist()))
    total_stock_list = []  # 10.18
    for single_code in weekly_code_list:
        # print(single_code)
        single_stock_data = pd.read_csv(daily_stock_path + zeroize.zeroize(single_code) + '.csv')
        single_stock_week_data = pd.read_csv(weekly_stock_path + zeroize.zeroize(single_code) + '.csv')
        # if len(single_stock_data) > 500 and len(single_stock_week_data) > 100:
        buy_observe_first_week = gd.get_first_observe_date(single_stock_data, week_end_date)
        buy_date_monday = gd.get_buy_date_10(single_stock_data, single_stock_week_data, buy_observe_first_week)
        if type(buy_observe_first_week) == int:
            buy_date_monday = gd.get_buy_date_10(single_stock_data,single_stock_week_data,buy_observe_first_week)
            # print(buy_date_monday)
            if (type(buy_date_monday)) == int:  # and ([single_code,buy_date_monday] in buy_stock_log):
                # 由于有可能存在连续好几天都出现doctor tao信号，而他们都是统一在同一天购买，因此会出现重复统计的情况，
                # 因此记录一下买入时间，以便去重
                # buy_stock_log.append([single_code,buy_date_monday])
                buy_date_index_daily = single_stock_data['trade_date'].tolist().index(buy_date_monday)
                buy_price = single_stock_data['high'].tolist()[buy_date_index_daily]  # 用最高价测试
                if (buy_date_index_daily + duration_day) <= len(single_stock_data):
                    highest_price = max(single_stock_data['high'].tolist()[buy_date_index_daily:(buy_date_index_daily + duration_day)])

                    sell_date_index = single_stock_data['high'].tolist()[buy_date_index_daily:(buy_date_index_daily + duration_day)].index(highest_price) + buy_date_index_daily
                    sell_date = single_stock_data['trade_date'].tolist()[sell_date_index]
                    if week_end_date == 20141219:
                        print('stock_code=' + str(single_code))
                        print('buy_date_index_daily = ' + str(buy_date_index_daily))
                        print('buy_date_index_daily + duration_day = ' + str(buy_date_index_daily + duration_day))
                        print(single_stock_data['high'].tolist()[buy_date_index_daily:(buy_date_index_daily + duration_day)])
                        print('highest_price='+ str(highest_price))
                        print('sell_date_index=' + str(sell_date_index))
                        print('sell_date' + str(sell_date))
                        print('------------------------------------------------------')
                else:
                    highest_price = max(single_stock_data['high'].tolist()
                                        [buy_date_index_daily:len(single_stock_data)])
                    sell_date_index = single_stock_data['high'].tolist()[
                                      buy_date_index_daily:len(single_stock_data)].index(highest_price)
                    sell_date = single_stock_data['trade_date'].tolist()[sell_date_index]
                increase_rate = (highest_price - buy_price) / buy_price
                '''
                if len([single_code, buy_date_monday, sell_date, sell_date_index - buy_date_index_daily,
                        buy_price, highest_price, increase_rate]) != 0:
                    total_stock_list.append(
                        [single_code, buy_date_monday, sell_date, sell_date_index - buy_date_index_daily,
                         buy_price, highest_price, increase_rate])
                '''
        total_stock_list.append([single_code, buy_date_monday, sell_date, sell_date_index - buy_date_index_daily,
                                 buy_price, highest_price, increase_rate])

    total_stock_df = pd.DataFrame(total_stock_list, columns=['code', 'buy_date', 'sell_date', 'duration(day)',
                                                             'buy_price', 'sell_price', 'increase_rate'])
    if len(total_stock_df) != 0:
        total_stock_df.to_csv(result_path + 'buy_under_10k/' + str(week_end_date) + '.csv', index=False)