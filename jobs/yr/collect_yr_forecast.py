#!/usr/bin/python3

import sys
import getopt
import os
import json
import requests
from requests_oauthlib import OAuth1 as oauth
from configobj import ConfigObj
import http.client, urllib.request, urllib.parse, urllib.error, base64


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
		print(data)
		conn.close()
	except Exception as e:
		print("[Errno {0}] {1}".format(e.errno, e.strerror))

	return json.loads(data.decode('utf-8'))


def main(argv):
	yr_data = get_yr_data()
	print(yr_data)

	with open('/home/pi/kratosdata/yr_forecast.json', 'w') as outfile:
		json.dump(yr_data, outfile)

if __name__ == "__main__":
	main(sys.argv[1:])