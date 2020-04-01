import pandas as pd

def get_week_start_date(last_week_end,daily_stock_path):
    data_orgin_1 = pd.read_csv(daily_stock_path + '/000001.csv')
    data_orgin_1_date_list = data_orgin_1['trade_date'].tolist()
    data_orgin_2 = pd.read_csv(daily_stock_path + '/600519.csv')
    data_orgin_2_date_list = data_orgin_2['trade_date'].tolist()
    # print(last_week_end)
    if last_week_end not in data_orgin_1_date_list:
        current_date_index = data_orgin_2_date_list.index(last_week_end)
        week_start_date = data_orgin_2_date_list[current_date_index]
    else:
        current_date_index = data_orgin_1_date_list.index(last_week_end)
        week_start_date = data_orgin_1_date_list[current_date_index]
    return week_start_date