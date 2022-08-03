#!/usr/bin/python3

import datetime
import pytz
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
	now=datetime.datetime.now(pytz.utc) 
	
	kratoslib.writeKratosLog('DEBUG', 'Collecting weConnect data...')
	weConnect = connect()
	
	batteryStatus=''
	chargingStatus=''
	chargingSettings=''
	plugStatus=''
	climatisationStatus=''
	readinessStatus=''
	for vin, vehicle in weConnect.vehicles.items():
		if vin == config['vin']:
			#print(vehicle)
			batteryStatus = vehicle.domains['charging']['batteryStatus']
			chargingStatus = vehicle.domains['charging']['chargingStatus']
			chargingSettings = vehicle.domains['charging']['chargingSettings']
			plugStatus = vehicle.domains['charging']['plugStatus']
			climatisationStatus = vehicle.domains['climatisation']['climatisationStatus']
			readinessStatus = vehicle.domains['readiness']['readinessStatus']

	# Store online and active status
	online=str(readinessStatus).split('\n')[2].split(':')[1].strip()

	# If not online, then just return.  Any data will be old
	kratoslib.writeStatuslogDataTime('weconnect.online', online, now)
	if online == 'False':
		kratoslib.writeKratosLog('WARN', 'weConnect: Car is offline')
		return False
	
	active=str(readinessStatus).split('\n')[3].split(':')[1].strip()
	kratoslib.writeStatuslogDataTime('weconnect.active', active, now)

	# Find SoC and Range
	soc=str(batteryStatus).split('\n')[1].split(':')[1][:-1].strip()
	range=str(batteryStatus).split('\n')[2].split(':')[1][:-2].strip()

	# Collect prior SoC and range before storing new values, this can be used to check if the car is moving
	range_last = range
	soc_last = soc
	try:
		range_last = int(kratoslib.readKratosData('weconnect.range'))
		soc_last = int(kratoslib.readKratosData('weconnect.soc'))
	except:
		pass
	kratoslib.writeTimeseriesDataTime('weconnect.soc', float(soc), now)
	kratoslib.writeTimeseriesDataTime('weconnect.range', float(range), now)

	# Store charging statue
	state=str(chargingStatus).split('\n')[1].split(':')[1].strip()
	remainingChargeTimeMinutes=int(str(chargingStatus).split('\n')[3].split(':')[1].split(' ')[1].strip())
	chargePower=float(str(chargingStatus).split('\n')[4].split(':')[1].split(' ')[1].strip())
	chargeRate=float(str(chargingStatus).split('\n')[5].split(':')[1].split(' ')[1].strip())
	kratoslib.writeStatuslogDataTime('weconnect.state', state, now)
	kratoslib.writeTimeseriesDataTime('weconnect.remainingChargeTime', remainingChargeTimeMinutes, now)
	kratoslib.writeTimeseriesDataTime('weconnect.chargePower', chargePower, now)
	kratoslib.writeTimeseriesDataTime('weconnect.chargeRate', chargeRate, now)

	# Store Target SoC for charging
	# Note: This does not include any different target set in a charging profile
	targetSoc=int(str(chargingSettings).split('\n')[4].split(':')[1].split(' ')[1].strip())
	kratoslib.writeTimeseriesDataTime('weconnect.targetSoc', targetSoc, now)
	
	# Store Plug status
	plug=str(plugStatus).split('\n')[1].split(':')[1].split(',')[0].strip()
	kratoslib.writeStatuslogDataTime('weconnect.plug', plug, now)

	# Store Climatisation Status
	climatisationState=str(climatisationStatus).split('\n')[1].split(':')[1].strip()
	kratoslib.writeStatuslogDataTime('weconnect.climatisationState', climatisationState, now)


	if kratoslib.readKratosData('weconnect.driving') == 'True':
		driving = True
		# Last time around, we found the car was driving.  Check if it still is
		if active == 'True':
			# Still driving
			distance = int(kratoslib.readKratosData('weconnect.rangeAtStart')) - int(range)
			if distance < 0:
				distance = 0
			kratoslib.writeKratosData('weconnect.currentDistance', str(distance))
		else:
			# Not driving anymore
			driving = False
			kratoslib.writeStatuslogDataTime('weconnect.driving', 'False', now)
	else:
		# Check if we are driving now
		if active == 'True' and plug == 'disconnected':
			driving = True
			distance = round(float(range) - float(range_last))
			if distance < 0:
				distance = 0
			kratoslib.writeStatuslogDataTime('weconnect.driving', 'True', now)
			kratoslib.writeKratosData('weconnect.rangeAtStart', str(range_last))
			kratoslib.writeKratosData('weconnect.currentDistance', str(distance))
		else:
			driving = False
			kratoslib.writeStatuslogDataTime('weconnect.driving', 'False', now)

	return driving
	

def main(argv):
	driving = collect()
	count = 0
	rushhour = False
	while (driving or rushhour) and count < 4:
		kratoslib.writeKratosLog('DEBUG', 'Rushour or weConnect Driving state discovered, looping every 2 minutes: ' + str(count))
		count = count + 1
		time.sleep(120)
		driving = collect()

if __name__ == "__main__":
	config = ConfigObj(kratoslib.getKratosConfigFilePath('weconnect.conf'))
	main(sys.argv[1:])

