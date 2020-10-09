import pandas as pd

result_path = 'D:/pydir/long_term/veri_result/veri_doctor_tao/' + str(70) + '/'

stock_data = pd.read_csv(result_path + '/raw/20140103.csv')
print(type(stock_data['date'].tolist()[0]))
a = stock_data['date'].tolist()[0]
print(a)
print(a%2000)