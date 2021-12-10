import datetime

tomorrow_period=(datetime.datetime.now() + datetime.timedelta(days=1)).strftime('%Y%m%d')
#tomorrow_period=datetime.datetime.strptime(tomorrow, '%Y%M%D%h%m')
print(tomorrow_period)