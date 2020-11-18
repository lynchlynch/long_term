import matplotlib.pyplot as plt
import mplfinance as mpf
import numpy as np
import pandas as pd
from matplotlib.pylab import date2num

daily_stock_path = 'D:/pydir/Raw Data/Tushare_pro/daily_data/'
data=pd.read_csv(daily_stock_path + '000001.csv',usecols=['trade_date','open','close','high','low','vol'])
data[data['vol']==0]=np.nan
data=data.dropna()
data.sort_values(by='trade_date',ascending=True,inplace=True)
data=data[['trade_date','open','close','high','low','vol']]
# print(data['trade_date'])
data['trade_date'] = pd.to_datetime(data['trade_date'])
data.set_index(['trade_date'],inplace=True)
print(data)

fig,ax=plt.subplots(figsize=(1200/72,480/72))
fig.subplots_adjust(bottom=0.1)
mpf.plot(data)
ax.grid(True)
ax.xaxis_date()
plt.show()