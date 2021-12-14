#!/usr/bin/python3

import sys
import getopt
import os
from configobj import ConfigObj
import xml.etree.ElementTree as ET
import mysql.connector
import datetime

import kratoslib


def save_da_price_now(connection):
	sql = ("SELECT CAST(ROUND(price,2) AS CHAR(6)) as price FROM dayahead WHERE pricedate=%s and period=%s ")
	hour = int(datetime.datetime.now().strftime('%H'))
	now = datetime.datetime.now().strftime('%Y-%m-%d')
	cursor=connection.cursor()
	period_data = (now, int(hour))
	cursor.execute(sql, period_data)
	price_eur = '0.0'
	for (price) in cursor:
		price_eur = price
	cursor.close()
	kratoslib.writeKratosLog('DEBUG', 'Hourly price for ' + now + '-' + str(hour) + ': ' + str(price_eur[0]))
	kratoslib.writeKratosData('powerprice.eur', str(price_eur[0]))


def main(argv):
	global config

	if ('user' not in config or config['user'] == ''):
		print('ERROR: Missing user')
		exit(1)

	connection = mysql.connector.connect(user=config['user'], password=config['password'],
                              host=config['host'],
                              database=config['database'])

	save_da_price_now(connection)

	connection.close()
	exit(0)

if __name__ == "__main__":
	config = ConfigObj(kratoslib.getKratosConfigFilePath('kratosdb.conf'))
	main(sys.argv[1:])