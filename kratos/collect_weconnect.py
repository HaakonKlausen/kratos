#!/usr/bin/python3

import sys
import time 

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

def collect():
	global config

	driving = False

	kratoslib.writeKratosLog('DEBUG', 'Collecting weConnect data...')
	weConnect = connect()
	
	batteryStatus=''
	chargingStatus=''
	chargingSettings=''
	plugStatus=''
	for vin, vehicle in weConnect.vehicles.items():
		if vin == config['vin']:
			#print(vehicle)
			batteryStatus = vehicle.domains['charging']['batteryStatus']
			chargingStatus = vehicle.domains['charging']['chargingStatus']
			chargingSettings = vehicle.domains['charging']['chargingSettings']
			plugStatus = vehicle.domains['charging']['plugStatus']

	soc=str(batteryStatus).split('\n')[1].split(':')[1][:-1].strip()
	range=str(batteryStatus).split('\n')[2].split(':')[1][:-2].strip()
	#print(soc, range)
	kratoslib.writeKratosData('weconnect.soc', str(soc))
	kratoslib.writeTimeseriesData('weconnect.soc', float(soc))
	kratoslib.writeKratosData('weconnect.range', str(range))
	kratoslib.writeTimeseriesData('weconnect.range', float(range))

	range_last = 0
	try:
		range_last = int(kratoslib.readKratosData('weconnect.range.last'))
	except:
		pass
	kratoslib.writeKratosData('weconnect.range.last', str(range))
	

	
	kratoslib.writeKratosData('weconnect.range.last', str(range))

	state=str(chargingStatus).split('\n')[1].split(':')[1].strip()
	remainingChargeTimeMinutes=str(chargingStatus).split('\n')[3].split(':')[1].split(' ')[1].strip()
	chargePower=str(chargingStatus).split('\n')[4].split(':')[1].split(' ')[1].strip()
	chargeRate=str(chargingStatus).split('\n')[5].split(':')[1].split(' ')[1].strip()
	#print(chargingStatus)
	#print(state, remainingChargeTimeMinutes, chargePower, chargeRate)
	kratoslib.writeKratosData('weconnect.state', state)
	kratoslib.writeKratosData('weconnect.remainingChargeTime', str(remainingChargeTimeMinutes))
	kratoslib.writeKratosData('weconnect.chargePower', str(chargePower))
	kratoslib.writeKratosData('weconnect.chargeRate', str(chargeRate))

	targetSoc=str(chargingSettings).split('\n')[3].split(':')[1].split(' ')[1].strip()
	#print(chargingSettings)
	#print(targetSoc)
	kratoslib.writeKratosData('weconnect.targetSoc', str(targetSoc))
	
	plug=str(plugStatus).split('\n')[1].split(':')[1].split(',')[0].strip()
	#print(plugStatus)
	#print(plug)
	kratoslib.writeKratosData('weconnect.plug', plug)

	kratoslib.writeKratosLog('INFO', 'weConnect SOC: ' + str(soc) + ' Range: ' + str(range))

	try:
		if int(chargePower) == 0 and range < range_last:
			driving = True
	except:
		kratoslib.writeKratosLog('ERROR', 'weConnect chargepower is not numeric')

	if driving:
		kratoslib.writeKratosData('weconnect.driving', 'True')
	else:
		kratoslib.writeKratosData('weconnect.driving', 'False')

	return driving
	
def main(argv):
	driving = collect()
	count = 0
	while driving and count < 4:
		kratoslib.writeKratosLog('DEBUG', 'weConnect Driving state discovered, looping every 2 minutes: ' + str(count))
		count = count + 1
		time.sleep(120)
		driving = collect()

if __name__ == "__main__":
	config = ConfigObj(kratoslib.getKratosConfigFilePath('weconnect.conf'))
	main(sys.argv[1:])

