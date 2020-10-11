import pandas as pd

import decide_disclosure_date as ddd

disclosure_df = pd.read_csv('D:/pydir/Raw Data/Tushare_pro/disclosure_date/total_disclosure.csv')
stock_code = int('000001')
buy_date = 20170413
process_date = ddd.decide_disclosure_date(stock_code,buy_date,disclosure_df)
# print(process_date)