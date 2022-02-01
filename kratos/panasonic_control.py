#!/usr/bin/python3
#
# Control the power usage and temperature of the Panasonic air-to-air heater
#
from configobj import ConfigObj
import datetime
import pytz
import json
import sys
import time

import pcomfortcloud

import kratoslib

def get_session():
	global config

	try:
		user=config['user']
		password=config['password']
		session = pcomfortcloud.Session(user, password, tokenFileName='/home/pi/.panasonic-token')
		session.login()
		return session
	except Exception as e:
		kratoslib.writeKratosLog('ERROR', 'Unable to create pcomfortcloud sesseion: ' + str(e))
		exit(1)

def get_id(session):
	try:
		devices = session.get_devices()
	except Exception as e:
		kratoslib.writeKratosLog('ERROR', 'Error in getting devices')
		print('Error in getting devices' + str(e))
		exit(1)

	id=devices[0]['id']
	return id


def get_info(session, id):
	try:
		device=session.get_device(id)
	except Exception as e:
		kratoslib.writeKratosLog('ERROR', 'Error in getting device info')
		print('Error in getting device info' + str(e))
		exit(1)

	#print(device)
	# {'id': '59a0c60fb6604818a6e29f1aa72d92be', 'parameters': 
	# 	{'temperatureInside': 22, 'temperatureOutside': 3, 'temperature': 21.0, 'power': <Power.On: 1>, 'mode': <OperationMode.Heat: 3>, 'fanSpeed': <FanSpeed.Auto: 0>, 'airSwingHorizontal': <AirSwingLR.Mid: 2>, 'airSwingVertical': <AirSwingUD.Mid: 2>, 'eco': <EcoMode.Auto: 0>, 'nanoe': <NanoeMode.On: 2>}}
	return device 

def get_power(info):
	power = info['parameters']['power']
	print(power)

def store_info(info):
	
	temperatureInside = float(info['parameters']['temperatureInside'])
	temperatureOutside = float(info['parameters']['temperatureOutside'])
	temperature = float(info['parameters']['temperature'])
	power = str(info['parameters']['power']).strip()

	now=datetime.datetime.now(pytz.utc)
	kratoslib.writeTimeseriesDataTime('panasonic.temperatureInside', temperatureInside, now)
	kratoslib.writeTimeseriesDataTime('panasonic.temperatureOutside', temperatureOutside, now)
	kratoslib.writeStatuslogDataTime('panasonic.power', power, now)
	# If power is off, we will just store 0 as temp
	if power != 'Power.On':
		temperature = 0
	kratoslib.writeTimeseriesDataTime('panasonic.temperature', temperature, now)

	return


def set_last_adjustment_time():
	kratoslib.writeKratosData('panasonic.lastadjustment.time', str(time.time()))

def get_last_adjustment_time():
	return float(kratoslib.readKratosData('panasonic.lastadjustment.time'))

def get_target_temperature():
	strdata = kratoslib.readKratosData('in.target_temperature')
	target_temperature=float(strdata)
	hour, minute = kratoslib.getHourMinute()
	if hour >=16 and hour < 22:
		# Warmer in the evening
		target_temperature = target_temperature + 0.0
	elif hour < 4:
		# Lower temperature at night
		target_temperature = target_temperature - 0.0

	return target_temperature

def get_panasonic_temperature():
	return float(kratoslib.readKratosData('panasonic.temperature'))

def get_average_in_temp():
	connection=kratoslib.getConnection()
	sql = ("select 60min_avg from in_temp_60min_avg order by created desc limit 7")
	last_avg = 0.0
	avg_60m = 0.0
	first = True
	cursor=connection.cursor()
	cursor.execute(sql)
	for val in cursor:
		if first:
			last_avg = float(val[0])
			first = False
		avg_60m = float(val[0])
	cursor.close()
	connection.close()
	return last_avg, avg_60m

def get_stored_average_in_temp():
	connection=kratoslib.getConnection()
	sql = ("select value from timeseries where seriesname='in.temp.avg120min' order by created desc limit 7")
	last_avg = 0.0
	avg_60m = 0.0
	first = True
	cursor=connection.cursor()
	cursor.execute(sql)
	for val in cursor:
		if first:
			last_avg = float(val[0])
			first = False
		avg_60m = float(val[0])
	cursor.close()
	connection.close()
	return last_avg, avg_60m


def adjustment_expired():
	if time.time() - get_last_adjustment_time() > 5250:
		return True
	else:
		return False

def set_temperature(session, id, new_temperature):
	session.set_device(id, temperature=new_temperature)
	set_last_adjustment_time()
	kratoslib.writeKratosLog('INFO', 'Panasonic: Changing Heatpump temperature to ' + str(new_temperature))
	kratoslib.writeKratosData('panasonic.temperature', str(new_temperature))
	

def averageAlgorithm():
	target_temperature = get_target_temperature()
	actual_temperature = float(kratoslib.readKratosData('in.temp'))
	average_temerature, last_average_temperature = get_stored_average_in_temp()
	# last_average_temperature = float(kratoslib.readKratosData('panasonic.lastadjustment.avg60'))
	panasonic_temperature = get_panasonic_temperature()
	new_panasonic_temperature = panasonic_temperature

	# Diff is how much the average temp differs from the desired temp of the room
	diff = average_temerature - target_temperature 
	# Change is how much the temperature has changed since we last checked
	# If there is a sizable change in the correct direction since we last checked, we do not want to adjust
	change = average_temerature - last_average_temperature

	kratoslib.writeTimeseriesData('panasonic.diff', diff)
	kratoslib.writeTimeseriesData('panasonic.change', change)
	#print('Target: ' + str(target_temperature) + ' Average: ' + str(average_temerature) + ' Panasonic: ' + str(panasonic_temperature) + ' Diff: ' + str(diff) + ' Change: ' + str(change))
	kratoslib.writeKratosLog('INFO', 'Panasonic Target: ' + str(target_temperature) + ' Average: ' + str(average_temerature) + ' Actual: ' + str(actual_temperature) + ' Panasonic: ' + str(panasonic_temperature) + ' Diff: ' + str(diff) + ' Change: ' + str(change))
	if diff > 0.2:
		kratoslib.writeKratosLog('DEBUG', 'Panasonic: Diff > 0.3')
		# Do not change if temp is on its way down by at least 0.1
		if change >= -0.2:
			kratoslib.writeKratosLog('DEBUG', 'Panasonic: Change >= -0.1')
			# Do not change of we are already below the actual temp, even if the average is higher
			if actual_temperature > target_temperature:
				kratoslib.writeKratosLog('DEBUG', 'Panasonic: actual temp > target')
				new_panasonic_temperature = panasonic_temperature - 0.5
	elif diff < -0.5:
		kratoslib.writeKratosLog('DEBUG', 'Panasonic: Diff < -0.3')
		# Do not change if temp is on its way up with at least 0.1
		if change <= 0.1:
			kratoslib.writeKratosLog('DEBUG', 'Panasonic: Change > = 0.1')
			# Do not change if we are already over the actual temp now, even if the averate is lower
			if actual_temperature < target_temperature:
				kratoslib.writeKratosLog('DEBUG', 'Panasonic: actual temp < target')
				new_panasonic_temperature = panasonic_temperature + 0.5
	elif actual_temperature < 19.5:
		new_panasonic_temperature = panasonic_temperature + 0.5
	else:
		kratoslib.writeKratosLog('INfO', 'Panasonic: Temperature within range, no change')

	return panasonic_temperature, new_panasonic_temperature


def actualAlgorithm():
	target_temperature = get_target_temperature()
	actual_temperature = float(kratoslib.readKratosData('in.temp'))
	panasonic_temperature = get_panasonic_temperature()
	new_panasonic_temperature = panasonic_temperature

def check_and_adjust(session, id):
	panasonic_temperature, new_panasonic_temperature = averageAlgorithm()

	# Safety valve
	# If the algorithm goes crazy, this will limit the setting
	if new_panasonic_temperature > 22:
		new_panasonic_temperature = 22
		kratoslib.writeKratosLog('INFO', 'Panasonic Prevented temp higher than 22')
	if new_panasonic_temperature < 19:
		new_panasonic_temperature = 19
		kratoslib.writeKratosLog('INFO', 'Panasonic Prevented temp less than 19')

	if new_panasonic_temperature != panasonic_temperature:
		kratoslib.writeKratosLog('DEBUG', 'Panasonic Potential temperature change to ' + str(new_panasonic_temperature))
		if adjustment_expired():
			set_temperature(session, id, new_panasonic_temperature)
			kratoslib.writeTimeseriesData('panasonic.temperature.adjusted', str(new_panasonic_temperature))
			#kratoslib.writeKratosData('panasonic.lastadjustment.avg60', str(average_temerature))
		else:
			kratoslib.writeKratosLog('DEBUG', 'Panasonic Adjustmenttime not yet expired')
			



def main(args):
	if len(args) == 0:
		print('USAGE: panasonic_control.py getinfo | storeinfo')
		exit(1)

	if args[0] == 'getinfo':
		session = get_session()
		id = get_id(session)
		info = get_info(session, id)
		print(info)
		print(info['parameters']['power'])

	if args[0] == 'storeinfo':
		session = get_session()
		id = get_id(session)
		info = get_info(session, id)
		store_info(info)

	if args[0] == 'adjust':
		session = get_session()
		id = get_id(session)
		info = get_info(session, id)
		store_info(info)
		check_and_adjust(session, id)
	
	if args[0] == 'avg':
		print(str(get_average_in_temp()))

	if args[0] == 'set':
		if len(args) < 2:
			print('ERROR: Missing temperature')
			exit(1)
		_new_temperature = 0.0
		try:
			_new_temperature = float(args[1])
		except:
			print('ERROR in temperature: ' + str(args[1]))
			exit(1)
		session = get_session()
		id = get_id(session)
		set_temperature(session, id, _new_temperature)

	if args[0] == 'power':
		session = get_session()
		id = get_id(session)
		info = get_info(session, id)
		get_power(info)

if __name__ == "__main__":
	config = ConfigObj(kratoslib.getKratosConfigFilePath('pcomfortcloud.conf'))
	main(sys.argv[1:])

