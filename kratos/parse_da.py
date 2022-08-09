#!/usr/bin/python3

import sys
import getopt
import os
from configobj import ConfigObj
import xml.etree.ElementTree as ET
import mysql.connector
import datetime

import kratoslib


def delete_da_prices(connection, date):
	print("Deleting old data...")
	sql = ("DELETE FROM dayahead WHERE pricedate='%s'")
	print(sql)
	data = (date.strftime('%Y-%m-%d'))
	print(data)
	cursor=connection.cursor()
	cursor.execute(sql, data)
	connection.commit()
	cursor.close()


def store_da_prices(connection, date):
	eur_rate = float(kratoslib.readKratosData('EUR'))
	print(eur_rate)
	sql = ("INSERT INTO dayahead (pricearea, pricedate, period, price, pricenok, pricenoknet) "
			"VALUES ('NO2', %s, %s, %s, %s, %s)")
	tree = ET.parse(kratoslib.getKratosConfigFilePath('da_forecast.xml'))
	hour = int(datetime.datetime.now().strftime('%H'))
	root = tree.getroot()
	cursor=connection.cursor()
	for period in range(24):
		print(root[9][7][period + 2][0].text, root[9][7][period + 2][1].text)
		price = float(root[9][7][period + 2][1].text)
		# Convert to NOK
		pricenok = price * eur_rate / 1000
		# Add LOS Price and MVA
		pricenok = (pricenok + 0.0345) * 1.25
		# Add Nettleie
		pricenoknet = pricenok + 0.4251
		if period >=6 and period < 22:
			pricenoknet = pricenoknet + 0.10
		period_data = (date, int(root[9][7][period + 2][0].text) - 1, root[9][7][period + 2][1].text, pricenok, pricenoknet)
		cursor.execute(sql, period_data)
		#if int(root[9][7][period + 2][0].text) == hour:
		#	writeKratosData('powerprice.eur', root[9][7][period + 2][1].text)
	connection.commit()
	cursor.close()


def main(argv):
	global config

	if ('user' not in config or config['user'] == ''):
		print('ERROR: Missing user')
		exit(1)
	
	tomorrow=(datetime.datetime.now() + datetime.timedelta(days=1))

	connection = mysql.connector.connect(user=config['user'], password=config['password'],
                              host=config['host'],
                              database=config['database'])

	delete_da_prices(connection, tomorrow)
	store_da_prices(connection, tomorrow)

	connection.close()
	exit(0)

if __name__ == "__main__":
	config = ConfigObj(kratoslib.getKratosConfigFilePath('kratosdb.conf'))
	main(sys.argv[1:])