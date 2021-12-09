#!/usr/bin/python3
# -*- coding: utf-8 -*-

import sys
import getopt
import os
import json
import requests
from requests_oauthlib import OAuth1 as oauth
from configobj import ConfigObj
import http.client, urllib.request, urllib.parse, urllib.error, base64


def get_marketstack_data():
	global config 

	headers = {
		# Request headers
	}


	params = urllib.parse.urlencode({'access_key': config['apikey'], 
                                    'symbols': config['symbols'],
                                    'limit': '1'
	})

	try:
		conn = http.client.HTTPConnection('api.marketstack.com')
		conn.request("GET", "/v1/eod?%s" % params, "{body}", headers)
		response = conn.getresponse()
		data = response.read()
		#print(data)
		conn.close()
	except Exception as e:
		print("[Errno {0}] {1}".format(e.errno, e.strerror))

	return json.loads(data.decode('utf-8'))


def parse_marketstack_data(marketstack_data):
	value = '0'
	dato_oppdatert = ''
	for data in marketstack_data['data']:
		value = data['close']
		dato_oppdatert = data['date']

	return value, dato_oppdatert


def writeKratosData(filename, value):
	filepath = "/home/pi/kratosdata/display/" + filename
	file = open(filepath, "w")
	file.write(value)
	file.close()


def main(argv):
	global config
	if ('apikey' not in config or config['apikey'] == ''):
		print('ERROR: No apikey in Config')
		return
	marketstack_data = get_marketstack_data()
	print(marketstack_data)
	value, dato_oppdatert = parse_marketstack_data(marketstack_data)

	writeKratosData('marketstack.tsla', str(value))
	writeKratosData('marketstack.date', str(dato_oppdatert))    
	print(value, dato_oppdatert)

if __name__ == "__main__":
	config = ConfigObj(os.path.expanduser('~') + '/.config/marketstack/marketstack.conf')
	main(sys.argv[1:])