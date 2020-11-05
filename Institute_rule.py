import tushare as ts

def institute_rule(stock_code,buy_date,end_date):
    ts.set_token('d34c57b1749de7df7766a60bb615078696e935856d99575c6b91bb5d')
    pro = ts.pro_api('d34c57b1749de7df7766a60bb615078696e935856d99575c6b91bb5d')
    fund_df = pro.