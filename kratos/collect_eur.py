#!/usr/bin/python3

import json
import http.client
import kratoslib
#
# API link from Norges Bank: https://data.norges-bank.no/api/data/EXR/B.EUR.NOK.SP?format=sdmx-json&lastNObservations=1&locale=no 

def fetch_eur_data():

	try:
		conn = http.client.HTTPSConnection('data.norges-bank.no')
		conn.request("GET", "/api/data/EXR/B.EUR.NOK.SP?format=sdmx-json&lastNObservations=1&locale=no", "{body}")
		response = conn.getresponse()
		data = response.read()
		conn.close()
	except Exception as e:
		print(e)

	return json.loads(data.decode('utf-8'))

def get_eur_data():
	rate = 0.0
	json = fetch_eur_data()
	for prop in json['data']['dataSets']:
		rate = prop['series']['0:0:0:0']['observations']['0'][0]
	return rate 


def main():
	rate = get_eur_data()
	kratoslib.writeTimeseriesData('EUR', rate)
	print(rate)

if __name__ == "__main__":
	main()