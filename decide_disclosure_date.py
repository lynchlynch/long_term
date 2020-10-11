#判断购买日期是否在财报披露之后，如果是之后，则可使用前一季度数据，若不是，则用前2季度数据
def decide_disclosure_date(stock_code,buy_date,disclosure_df):
    date_month_day = buy_date%2000
    year = int(buy_date / 10000)
    if date_month_day >= 101 and date_month_day <= 331:
        finance_end_date = str(year) + '1231'
        actual_disclosure_date = disclosure_df[(disclosure_df['stock_code'] == stock_code) &
                                               (disclosure_df['end_date'] == finance_end_date)]['actual_date'].tolist()[0]
        if buy_date > actual_disclosure_date:
            process_finance_date = finance_end_date
        else:
            process_finance_date =  str(year) + '0930'
    elif date_month_day >= 401 and date_month_day <= 630:
        finance_end_date = str(year) + '0331'
        print(finance_end_date)
        print(disclosure_df[(disclosure_df['stock_code'] == stock_code)])
        print(disclosure_df[(disclosure_df['stock_code'] == stock_code) & (disclosure_df['end_date'] == finance_end_date)])
        actual_disclosure_date = disclosure_df[(disclosure_df['stock_code'] == stock_code) &
                                               (disclosure_df['end_date'] == finance_end_date)]['actual_date'].tolist()[0]
        if buy_date > actual_disclosure_date:
            process_finance_date = finance_end_date
        else:
            process_finance_date =  str(year) + '1231'
    elif date_month_day >= 701 and date_month_day <= 930:
        finance_end_date = str(year) + '0630'
        actual_disclosure_date = disclosure_df[(disclosure_df['stock_code'] == stock_code) &
                                               (disclosure_df['end_date'] == finance_end_date)]['actual_date'].tolist()[0]
        if buy_date > actual_disclosure_date:
            process_finance_date = finance_end_date
        else:
            process_finance_date =  str(year) + '0331'
    elif date_month_day >= 1001 and date_month_day <= 1231:
        finance_end_date = str(year) + '0930'
        actual_disclosure_date = disclosure_df[(disclosure_df['stock_code'] == stock_code) &
                                               (disclosure_df['end_date'] == finance_end_date)]['actual_date'].tolist()[0]
        if buy_date > actual_disclosure_date:
            process_finance_date = finance_end_date
        else:
            process_finance_date = str(year) + '0630'
    else:
        print('wrong date:' + str(buy_date))
        process_finance_date = 0xfff

    return process_finance_date