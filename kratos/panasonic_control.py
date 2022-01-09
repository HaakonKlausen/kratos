#!/usr/bin/python3
#
# Control the power usage and temperature of the Panasonic air-to-air heater
#
from configobj import ConfigObj
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
		print('Unable to create pcomfortcloud sesseion: ' + str(e))
		kratoslib.writeKratosLog('ERROR', 'Unable to create pcomfortcloud sesseion: ' + str(e))
		exit(1)

def get_id(session):
	try:
		devices = session.get_devices()
	except Exception as e:
		kratoslib.writeKratosLog('ERROR', 'Error in getting devices')
		print('Error in getting devices' + str(e))
		exit(1)

	#print(devices)
	# [{'id': '59a0c60fb6604818a6e29f1aa72d92be', 'name': 'Stue', 'group': 'My House', 'model': ''}]
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

def store_info(info):
	#json_str="{'id': '59a0c60fb6604818a6e29f1aa72d92be', 'parameters': {'temperatureInside': 22, 'temperatureOutside': 3, 'temperature': 21.0, 'power': <Power.On: 1>, 'mode': <OperationMode.Heat: 3>, 'fanSpeed': <FanSpeed.Auto: 0>, 'airSwingHorizontal': <AirSwingLR.Mid: 2>, 'airSwingVertical': <AirSwingUD.Mid: 2>, 'eco': <EcoMode.Auto: 0>, 'nanoe': <NanoeMode.On: 2>}}"
	#info = get_info()

	temperatureInside = float(info['parameters']['temperatureInside'])
	temperatureOutside = float(info['parameters']['temperatureOutside'])
	temperature = float(info['parameters']['temperature'])
	
	kratoslib.writeTimeseriesData('panasonic.temperatureInside', temperatureInside)
	kratoslib.writeTimeseriesData('panasonic.temperatureOutside', temperatureOutside)
	kratoslib.writeTimeseriesData('panasonic.temperature', temperature)
	kratoslib.writeKratosData('panasonic.temperature', str(temperature))


	return info 


def set_last_adjustment_time():
	kratoslib.writeKratosData('panasonic.lastadjustment.time', str(time.time()))

def get_last_adjustment_time():
	return float(kratoslib.readKratosData('panasonic.lastadjustment.time'))

def adjustment_expired():
	if time.time() - get_last_adjustment_time() > 30:
		return True
	else:
		return False

def set_temperature(session, id, new_temperature):
	session.set_device(id, temperature=new_temperature)
	set_last_adjustment_time()


def check_and_adjust(session, id):
	if adjustment_expired():
		set_temperature(session, id, 19.5)
	else:
		print('Not yet')


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
		check_and_adjust(session, id)
		info = get_info(session, id)
		store_info(info)
		

if __name__ == "__main__":
	config = ConfigObj(kratoslib.getKratosConfigFilePath('pcomfortcloud.conf'))
	main(sys.argv[1:])

