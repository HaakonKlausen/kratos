#!/usr/bin/python3

import sys
import getopt
import os
from configobj import ConfigObj
import xml.etree.ElementTree as ET
import mysql.connector
import datetime
import json
import kratoslib


def writePowerPriceToJSON(value:float):
	filepath=os.path.join('/var/www/html/kratosdata', 'period_power_price.json')
	file = open(filepath, "w")
	power_json = {
		"period_power_price": float(value),
		"id": "period.powerprice01",
		"name": "Period Power Price",
		"connected": "true"
	}
	power_json_readable = json.dumps(power_json, indent=4)
	file.write(power_json_readable)
	file.close()
	kratoslib.pushWWWFileToBjonntjonn("period_power_price.json")

def save_da_price_now(connection):
	sql = ("SELECT CAST(ROUND(price,2) AS CHAR(6)) as price FROM dayahead WHERE pricedate=%s and period=%s and pricearea=%s")
	hour = int(datetime.datetime.now().strftime('%H'))
	now = datetime.datetime.now().strftime('%Y-%m-%d')
	cursor=connection.cursor()
	period_data = (now, int(hour), config['display_pricearea'])
	cursor.execute(sql, period_data)
	price_eur = '0.0'
	for (price) in cursor:
		price_eur = price[0]
	cursor.close()
	kratoslib.writeKratosLog('DEBUG', 'Hourly price for ' + now + '-' + str(hour) + ': ' + str(price_eur[0]))
	kratoslib.writeKratosData('powerprice.eur', str(price_eur[0]))

def export_da_pricenoknet_now(connection):
	sql = ("SELECT ROUND(pricenoknet,2) as pricenoknet FROM dayahead WHERE pricedate=%s and period=%s and pricearea=%s")
	hour = int(datetime.datetime.now().strftime('%H'))
	now = datetime.datetime.now().strftime('%Y-%m-%d')
	cursor=connection.cursor()
	period_data = (now, int(hour), config['display_pricearea'])
	cursor.execute(sql, period_data)
	price_nok_net = 0.0
	for (pricenoknet) in cursor:
		price_nok_net = pricenoknet[0]
		break
	cursor.close()
	writePowerPriceToJSON(price_nok_net)

def save_max_price_today(connection):
	# Get max price
	sql = ("SELECT CAST(ROUND(max(price),2) AS CHAR(6)) as price, period FROM dayahead WHERE pricedate=%s and pricearea=%s GROUP BY period  ORDER BY max(price) desc")
	now = datetime.datetime.now().strftime('%Y-%m-%d')
	cursor=connection.cursor()
	period_data = (now, config['display_pricearea'])
	cursor.execute(sql, period_data)
	price_eur = '0.0'
	price_eur3 = '0.0'
	period_max = 0
	rank = 0
	for (price, period) in cursor:
		if rank == 0:
			price_eur = price
			period_max = period 
		if rank == 2:
			price_eur3 = price
		rank = rank + 1
		if rank > 2:
			break
	try:
		cursor.close()
	except:
		pass
	kratoslib.writeKratosLog('DEBUG', 'Max price for today: ' + now + '-' + str(period_max) + ': ' + str(price_eur))
	kratoslib.writeKratosData('powerprice_max.eur', str(price_eur))
	kratoslib.writeKratosData('powerprice_max.period', str(period_max))
	kratoslib.writeKratosData('powerprice_3max.eur', str(price_eur3))


def main(argv):
	global config

	if ('user' not in config or config['user'] == ''):
		kratoslib.writeKratosLog('ERROR', 'Get Hourly Powerrice: ERROR: Missing user')
		exit(1)

	connection = mysql.connector.connect(user=config['user'], password=config['password'],
                              host=config['host'],
                              database=config['database'])

	save_da_price_now(connection)
	save_max_price_today(connection)
	connection.close()

	connection = mysql.connector.connect(user=config['user'], password=config['password'],
                              host=config['host'],
                              database=config['database'])
	export_da_pricenoknet_now(connection)
	connection.close()
	exit(0)

if __name__ == "__main__":
	config = ConfigObj(kratoslib.getKratosConfigFilePath('kratosdb.conf'))
	main(sys.argv[1:])