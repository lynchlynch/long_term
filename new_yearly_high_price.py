import pandas as pd

def new_yearly_high_price(stock_path,stock_code,threshold,current_process_date):
    stock_data = pd.read_csv(stock_path + '/' + stock_code + '.csv')
    index = stock_data[stock_data['trade_date']==current_process_date].index.values[0]
    highest_yearly_price = max(stock_data['high'][index-250+1:index+1])
    return stock_data['close'][index]/highest_yearly_price >= threshold