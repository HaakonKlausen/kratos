#!/usr/bin/python3
# -*- coding: utf-8 -*-

import getopt
import json
import os
import requests

import sys
from configobj import ConfigObj
import http.client, urllib.request, urllib.parse, urllib.error, base64
from requests_oauthlib import OAuth1 as oauth

import kratoslib

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



def main(argv):
	global config
	
	kratoslib.writeKratosLog('DEBUG', 'Collecting Marketstack close')
	if ('apikey' not in config or config['apikey'] == ''):
		kratoslib.writeKratosLog('ERROR', 'No apikey in Config marketstack.conf')
		exit(1)
	marketstack_data = get_marketstack_data()
	value, dato_oppdatert = parse_marketstack_data(marketstack_data)

	prior_value = kratoslib.readKratosData('marketstack.tsla')
	if float(value) < float(prior_value):
		kratoslib.writeKratosData('marketstack.tsla.direction', 'down')
	else:
		# Equal = Up :-)
		kratoslib.writeKratosData('marketstack.tsla.direction', 'up')

	kratoslib.writeKratosData('marketstack.date', str(dato_oppdatert))   

	kratoslib.writeTimeseriesData('marketstack.tsla', value) 

if __name__ == "__main__":
	config = ConfigObj(kratoslib.getKratosConfigFilePath('marketstack.conf'))
	main(sys.argv[1:])