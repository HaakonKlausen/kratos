import sys
import getopt
import os
from configobj import ConfigObj
import xml.etree.ElementTree as ET
import mysql.connector
import datetime



def delete_da_prices(connection, date):
	sql = ("DELETE FROM dayahead WHERE pricedate='%s'")
	data = (date)
	cursor=connection.cursor()
	cursor.execute(sql, data)
	connection.commit()
	cursor.close()


def store_da_prices(connection, date):
	sql = ("INSERT INTO dayahead (pricedate, period, price) "
			"VALUES (%s, %s, %s)")
	tree = ET.parse("/home/pi/kratosdata/da_forecast.xml")
	root = tree.getroot()
	cursor=connection.cursor()
	for period in range(24):
		print(root[9][7][period + 2][0].text, root[9][7][period + 2][1].text)
		period_data = (date, int(root[9][7][period + 2][0].text) - 1, root[9][7][period + 2][1].text)
		cursor.execute(sql, period_data)
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
	config = ConfigObj(os.path.expanduser('~') + '/.config/kratos/kratosdb.config')
	main(sys.argv[1:])