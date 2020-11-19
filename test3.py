import datetime as dt

sday = dt.date(2016, 6, 29)
eday = dt.date(2017, 1, 30)
print(int((eday - sday).days / 365.25))
a = sday + dt.timedelta(days=0)
print(a)