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


def get_da_data():
	global config

	tomorrow_period=(datetime.datetime.now() + datetime.timedelta(days=1)).strftime('%Y%m%d')
	headers = {
		# Request headers
	}
	params = urllib.parse.urlencode({
		'documentType': 'A44',
        'in_Domain': '10YNO-2--------T',
        'out_Domain': '10YNO-2--------T',
        'periodStart': tomorrow_period + '0000',
        'periodEnd': tomorrow_period + '2300',
        'securityToken': config['api_token']
	})

# urlApi = "'transparency.entsoe.eu/api?documentType=A44&in_Domain=10YNO-2--------T&out_Domain=10YNO-2--------T&periodStart="..year..month..day.."0000&periodEnd="..year..month..day.."2300&securityToken=SETT-INN-DIN-TOKEN-HER'"

	try:
		conn = http.client.HTTPSConnection('transparency.entsoe.eu')
		conn.request("GET", "/api?%s" % params, "{body}", headers)
		response = conn.getresponse()
		data = str(response.read())
		conn.close()
	except Exception as e:
		print("[Errno {0}] {1}".format(e.errno, e.strerror))

	return data #json.loads(data.decode('utf-8'))



def main(argv):
	global config

	if ('api_token' not in config or config['api_token'] == ''):
		print('ERROR: Missing api_token')
		exit(1)
		

	da_data = get_da_data()
    
	da_data = da_data.replace('\\n', '')
	da_data = da_data.replace('\\t', '')
	print(da_data)
	with open('/home/pi/kratosdata/da_forecast.xml', 'w') as outfile:
			outfile.write(da_data[2:-1])
	exit(0)

if __name__ == "__main__":
	config = ConfigObj(os.path.expanduser('~') + '/.config/entsoe/entsoe.config')
	main(sys.argv[1:])