#!/usr/bin/python3

import sys
import getopt
import os
import json
import requests
from requests_oauthlib import OAuth1 as oauth
from configobj import ConfigObj
import http.client, urllib.request, urllib.parse, urllib.error, base64
import pytz
import datetime

def setExpired(expires_str):
    with open('/home/pi/kratosdata/yr_expires.txt', 'w') as f:
       f.write(expires_str)

def get_yr_data():

	headers = {
		# Request headers
		'User-Agent': 'Kratos/0.1 hakon.klausen@icloud.com',
	}
	params = urllib.parse.urlencode({
	})

	try:
		conn = http.client.HTTPSConnection('api.met.no')
		conn.request("GET", "/weatherapi/locationforecast/2.0/compact?altitude=0&lat=58.14&lon=7.99&%s" % params, "{body}", headers)
		response = conn.getresponse()
		data = response.read()
		expires = response.getheader('Expires')
		setExpired(expires)
		print('Expires: ' + expires)
		conn.close()
	except Exception as e:
		print("[Errno {0}] {1}".format(e.errno, e.strerror))

	return json.loads(data.decode('utf-8'))




def getExpired():
    expires_str = ''
    with open('/home/pi/kratosdata/yr_expires.txt') as f:
        expires_str = f.readline().strip()
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



def main(argv):
	if hasExpired(getExpired()):
		yr_data = get_yr_data()
		with open('/home/pi/kratosdata/yr_forecast.json', 'w') as outfile:
			json.dump(yr_data, outfile)
	else:
		print('Previous query has not expired yet')
		exit(1)
	
	exit(0)

if __name__ == "__main__":
	main(sys.argv[1:])