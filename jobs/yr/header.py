import datetime
import pytz

expires_str = 'Thu, 09 Dec 2021 11:23:17 GMT'

def getExpired():
    expires_str = ''
    with open('/home/pi/kratosdata/yr_expires.txt') as f:
        expires_str = f.readline().strip()
        print(expires_str)
    return expires_str


def expirestime2osl(expires_str):
    gmt_timezone=pytz.timezone('GMT')
    expires_date = gmt_timezone.localize(datetime.datetime.strptime(expires_str, '%a, %d %b %Y %H:%M:%S %Z'))
    osl_timezone=pytz.timezone('Europe/Oslo')
    expires_date_osl = expires_date.astimezone(osl_timezone)
    return expires_date_osl


def hasExpired(expires_str):
    expires_date = expirestime2osl(expires_str)
    osl_timezone=pytz.timezone('Europe/Oslo')
    now = datetime.datetime.now().astimezone(osl_timezone)
    if now > expires_date:
        return True
    else:
        return False


def setExpired(expires_str):
    with open('/home/pi/kratosdata/yr_expires.txt', 'w') as f:
       f.write(expires_str)

setExpired(expires_str)

if hasExpired(getExpired()):
    print('We can query')
else:
    print('Has to wait!')