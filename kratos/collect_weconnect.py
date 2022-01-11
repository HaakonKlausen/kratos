#!/usr/bin/python3

import sys

from configobj import ConfigObj
from weconnect import weconnect

import kratoslib

def connect():
	global config
	username=config['username']
	password=config['password']
	weConnect = weconnect.WeConnect(username=username, password=password,  tokenfile='/home/pi/.weconnect.token', updateAfterLogin=False, loginOnInit=True)
	weConnect.update()
	return weConnect

def main(argv):
	kratoslib.writeKratosLog('DEBUG', 'Collecting weConnect data...')
	weConnect = connect()
	
	batteryStatus=str('')
	for vin, vehicle in weConnect.vehicles.items():
		batteryStatus = vehicle.domains['charging']['batteryStatus']
		#print(vehicle.domains['charging']['batteryStatus'])

	soc=str(batteryStatus).split('\n')[1].split(':')[1][:-1]
	range=str(batteryStatus).split('\n')[2].split(':')[1][:-2]

	print(soc, range)
	kratoslib.writeKratosData('weconnect.soc', str(soc))
	kratoslib.writeTimeseriesData('weconnect.soc', float(soc))

	kratoslib.writeKratosData('weconnect.range', str(range))
	kratoslib.writeTimeseriesData('weconnect.range', float(range))

	kratoslib.writeKratosLog('INFO', 'weConnect SOC: ' + str(soc) + ' Range: ' + str(range))

if __name__ == "__main__":
	config = ConfigObj(kratoslib.getKratosConfigFilePath('weconnect.conf'))
	main(sys.argv[1:])

