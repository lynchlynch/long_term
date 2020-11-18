import mplfinance as mpf
import matplotlib as mpl# 用于设置曲线参数
from cycler import cycler# 用于定制线条颜色
import pandas as pd# 导入DataFrame数据
import matplotlib.pyplot as plt

daily_stock_path = 'D:/pydir/Raw Data/Tushare_pro/daily_data/'
result_path = 'D:/pydir/long_term/veri_result/veri_doctor_tao/'

def import_csv(stock_code):
    # 导入股票数据
    df = pd.read_csv(daily_stock_path + stock_code + '.csv')
    # 格式化列名，用于之后的绘制
    df.rename(
        columns={
            'trade_date': 'Date', 'open': 'Open',
            'high': 'High', 'low': 'Low',
            'close': 'Close', 'vol': 'Volume'},
        inplace=True)
    # 转换为日期格式
    df['Date'] = pd.to_datetime(df['Date'])
    # 将日期列作为行索引
    df.set_index(['Date'], inplace=True)
    return df


# 导入数据
symbol = '000001'
period = 100
df = import_csv(symbol)[-period:]
print(df.columns)

# 设置基本参数
# type:绘制图形的类型,有candle, renko, ohlc, line等
# 此处选择candle,即K线图
# mav(moving average):均线类型,此处设置7,30,60日线
# volume:布尔类型，设置是否显示成交量，默认False
# title:设置标题
# y_label:设置纵轴主标题
# y_label_lower:设置成交量图一栏的标题
# figratio:设置图形纵横比
# figscale:设置图形尺寸(数值越大图像质量越高)
kwargs = dict(
    type='candle',
    mav=(7, 30, 60),
    volume=True,
    title='\nA_stock %s candle_line' % (symbol),
    ylabel='OHLC Candles',
    ylabel_lower='Shares\nTraded Volume',
    figratio=(15, 10),
    figscale=5)

# 设置marketcolors
# up:设置K线线柱颜色，up意为收盘价大于等于开盘价
# down:与up相反，这样设置与国内K线颜色标准相符
# edge:K线线柱边缘颜色(i代表继承自up和down的颜色)，下同。详见官方文档)
# wick:灯芯(上下影线)颜色
# volume:成交量直方图的颜色
# inherit:是否继承，选填
mc = mpf.make_marketcolors(
    up='red',
    down='green',
    edge='i',
    wick='i',
    volume='in',
    inherit=True)

# 设置图形风格
# gridaxis:设置网格线位置
# gridstyle:设置网格线线型
# y_on_right:设置y轴位置是否在右
s = mpf.make_mpf_style(
    gridaxis='both',
    gridstyle='-.',
    y_on_right=False,
    marketcolors=mc)

# 设置均线颜色，配色表可见下图
# 建议设置较深的颜色且与红色、绿色形成对比
# 此处设置七条均线的颜色，也可应用默认设置
mpl.rcParams['axes.prop_cycle'] = cycler(
    color=['dodgerblue', 'deeppink',
           'navy', 'teal', 'maroon', 'darkorange',
           'indigo'])

# 设置线宽
mpl.rcParams['lines.linewidth'] = .5

# 图形绘制
# show_nontrading:是否显示非交易日，默认False
# savefig:导出图片，填写文件名及后缀
mpf.plot(df,
         **kwargs,
         style=s,
         show_nontrading=False,
         savefig=result_path + 'A_stock-%s %s_candle_line'
                 % (symbol, period) + '.jpg')
plt.show()