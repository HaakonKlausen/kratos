import datetime

tomorrow_period=(datetime.datetime.now() + datetime.timedelta(days=1)).strftime('%H')
#tomorrow_period=datetime.datetime.strptime(tomorrow, '%Y%M%D%h%m')
print(tomorrow_period)

hour = datetime.datetime.now().strftime('%H')
print(hour)