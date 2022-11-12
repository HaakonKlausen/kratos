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
	sqlstr = f"DELETE FROM dayahead WHERE pricedate = '{date.strftime('%Y-%m-%d')}'"
	sql = (sqlstr)
	cursor=connection.cursor()
	cursor.execute(sql)
	connection.commit()
	cursor.close()


def find_average_spot(connection, date):
	average_spot = 0.0
	sqlstr = f"SELECT AVG (pricenok) from dayahead where pricearea='NO2' and pricedate >= '{date.strftime('%Y-%m-01')}'"
	sql = (sqlstr)
	cursor=connection.cursor()
	cursor.execute(sql)
	for row in cursor:
		average_spot=row[0]
	cursor.close()
	return average_spot


def update_support_price(connection, date):
	average_spot = find_average_spot(connection, date)
	powersupport = 0.0
	powersupport = ((float(average_spot)) - 0.70) * 0.9 * 1.25
	if powersupport < 0.0:
		powersupport = 0.0
	sqlstr = f"UPDATE dayahead SET pricenoknetsupport = pricenoknet - {powersupport}  WHERE pricedate >= '{date.strftime('%Y-%m-01')}'"
	sql = (sqlstr)
	cursor=connection.cursor()
	cursor.execute(sql)
	connection.commit()
	cursor.close()
	kratoslib.writeTimeseriesData('gjennomsnitt_spotpris', average_spot)
	kratoslib.writeTimeseriesData('stromstotte_belop', powersupport)
	


def store_da_prices(connection, date):
	eur_rate = float(kratoslib.readKratosData('EUR'))
	print(eur_rate)
	sql = ("INSERT INTO dayahead (pricearea, pricedate, period, price, pricenok, pricenoklos, pricenoknet) "
			"VALUES ('NO2', %s, %s, %s, %s, %s, %s)")
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
		pricenoklos = (pricenok + 0.0345) * 1.25
		# Add Nettleie
		pricenoknet = pricenoklos + 0.4251
		if period >=6 and period < 22:
			pricenoknet = pricenoknet + 0.10
		period_data = (date, int(root[9][7][period + 2][0].text) - 1, root[9][7][period + 2][1].text, pricenok, pricenoklos, pricenoknet)
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
	update_support_price(connection, tomorrow)
	connection.close()
	exit(0)

if __name__ == "__main__":
	config = ConfigObj(kratoslib.getKratosConfigFilePath('kratosdb.conf'))
	main(sys.argv[1:])