import pandas as pd
import os

# import

def A_rule(finance_data_path,stock_code,buy_date):
    disclosure_result_path = 'D:/pydir/Raw Data/Tushare_pro/disclosure_date/'
    disclosure_result_data = pd.read_csv(disclosure_result_path + 'total_disclosure.csv')
    # report_date = disclosure_result_data[(disclosure_result_data['stock_code'] == int(stock_code)) and ]
    # print('--------------'+stock_code+'----------------')
    if os.path.exists(finance_data_path + stock_code + '.csv'):
        select_df = disclosure_result_data[disclosure_result_data['stock_code'] == int(stock_code)]
        select_df = select_df.reset_index(drop=True)
        for index in range(len(select_df)-1):
            if (int(select_df['actual_date'].tolist()[index]) < int(buy_date)) and \
                    (int(select_df['actual_date'].tolist()[index+1]) >= int(buy_date)):
                end_date = select_df['end_date'].tolist()[index]
                break
        if int(buy_date) >= int(select_df['actual_date'].tolist()[len(select_df)-1]):
            end_date = select_df['end_date'].tolist()[len(select_df)-1]
        year =int((end_date - (end_date % 1000)) / 10000)
        year_date_1 = year * 10000 + 1231
        year_date_2 = (year - 1) * 10000 + 1231
        year_date_3 = (year - 2) * 10000 + 1231
        stock_finance_data = pd.read_csv(finance_data_path + stock_code + '.csv')
        # select_index = stock_finance_data['end_date'].tolist().index(int(end_date))
        year_date_1_index = stock_finance_data['end_date'].tolist().index(int(year_date_1))
        year_date_2_index = stock_finance_data['end_date'].tolist().index(int(year_date_2))
        year_date_3_index = stock_finance_data['end_date'].tolist().index(int(year_date_3))
        eps_yoy_list = stock_finance_data['basic_eps_yoy'].tolist()
        eps_current = eps_yoy_list[year_date_1_index]
        eps_pre_1 = eps_yoy_list[year_date_2_index]
        eps_pre_2 = eps_yoy_list[year_date_3_index]

        #收益增长率25-50
        if (eps_current > 25) and eps_pre_1 > 25 and eps_pre_2 > 25:
            satisfy_a_rule_eps = 'True'
        else:
            satisfy_a_rule_eps = 'False'

        #股本回报率
        eps_yoy_list = stock_finance_data['roe'].tolist()
        roe_1 = eps_yoy_list[year_date_1_index]
        roe_2 = eps_yoy_list[year_date_2_index]
        roe_3 = eps_yoy_list[year_date_3_index]
        if roe_1 > 17 and roe_2 > 17 and roe_3 > 17:
            satisfy_a_rule_roe = 'True'
        else:
            satisfy_a_rule_roe = 'False'

        if satisfy_a_rule_eps == 'True' and satisfy_a_rule_roe == 'True':
            satisfy_a_rule = 'True'
        else:
            satisfy_a_rule = 'False'
    else:
        satisfy_a_rule = 'N'

    return satisfy_a_rule

