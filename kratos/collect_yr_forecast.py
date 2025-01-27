#!/usr/bin/python3

import datetime
import getopt
import json
import os
import requests
import sys

from requests_oauthlib import OAuth1 as oauth
from configobj import ConfigObj
import http.client, urllib.request, urllib.parse, urllib.error, base64
import pytz

import kratoslib


def setExpired(expires_str):
	with open(kratoslib.getKratosConfigFilePath('yr_expires.txt'), 'w')  as f:
		f.write(expires_str)

def get_yr_data():
	global config

	headers = {
		# Request headers
		'User-Agent': config['useragent_app'] + ' ' + config['useragent_contact'] #'Kratos/0.1 hakon.klausen@icloud.com',
	}
	params = urllib.parse.urlencode({
		'altitude': config['altitude'],
		'lat': config['lat'],
		'lon': config['lon']
	})

	try:
		conn = http.client.HTTPSConnection('api.met.no')
		conn.request("GET", "/weatherapi/locationforecast/2.0/compact?%s" % params, "{body}", headers)
		response = conn.getresponse()
		data = response.read()
		expires = response.getheader('Expires')
		setExpired(expires)
		print('Expires: ' + expires)
		conn.close()
	except Exception as e:
		kratoslib.writeKratosLog('ERROR', "Collect YR Forecast: [Errno {0}] {1}".format(e.errno, e.strerror))

	return json.loads(data.decode('utf-8'))




def getExpired():
    expires_str = ''
    with open(kratoslib.getKratosConfigFilePath('yr_expires.txt')) as f:
        expires_str = f.readline().strip()
    return expires_str


def expirestime2osl(expires_str):
	gmt_timezone=pytz.timezone('GMT')
	if expires_str == '':
		expires_date = gmt_timezone.localize(datetime.datetime.now())
	else:
		expires_date = gmt_timezone.localize(datetime.datetime.strptime(expires_str, '%a, %d %b %Y %H:%M:%S %Z'))
	osl_timezone=pytz.timezone('Europe/Oslo')
	expires_date_osl = expires_date.astimezone(osl_timezone)
	return expires_date_osl


def hasExpired(expires_str):
	if expires_str == '':
		return True
	expires_date = expirestime2osl(expires_str)
	osl_timezone=pytz.timezone('Europe/Oslo')
	now = datetime.datetime.now().astimezone(osl_timezone)
	if now > expires_date:
		return True
	else:
		return False



def main(argv):
	global config

	if ('useragent_contact' not in config or config['useragent_contact'] == ''):
		kratoslib.writeKratosLog('ERROR', 'Missing config in yr.conf')
		exit(1)
		
	if hasExpired(getExpired()):
		yr_data = get_yr_data()
		with open(kratoslib.getKratosConfigFilePath('yr_forecast.json'), 'w') as outfile:
			json.dump(yr_data, outfile)
	else:
		kratoslib.writeKratosLog('DEBUG', 'Yr: Previous query has not expired yet')
		exit(1)
	
	exit(0)

if __name__ == "__main__":
	config = ConfigObj(kratoslib.getKratosConfigFilePath('yr.conf'))
	main(sys.argv[1:])