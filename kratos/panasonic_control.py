#!/usr/bin/python3
#
# Control the power usage and temperature of the Panasonic air-to-air heater
#
import sys
from configobj import ConfigObj
import json

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
		print('Error in login: ' + str(e))
		exit(1)

def get_info():
	session = get_session()
	try:
		devices = session.get_devices()
	except Exception as e:
		kratoslib.writeKratosLog('Error', 'Error in getting devices')
		print(str(e))
		exit(1)

	#print(devices)
	# [{'id': '59a0c60fb6604818a6e29f1aa72d92be', 'name': 'Stue', 'group': 'My House', 'model': ''}]
	id=devices[0]['id']
	#print(id)
	try:
		device=session.get_device(id)
	except Exception as e:
		kratoslib.writeKratosLog('Error', 'Error in getting device info')
		print(str(e))
		exit(1)

	#print(device)
	# {'id': '59a0c60fb6604818a6e29f1aa72d92be', 'parameters': 
	# 	{'temperatureInside': 22, 'temperatureOutside': 3, 'temperature': 21.0, 'power': <Power.On: 1>, 'mode': <OperationMode.Heat: 3>, 'fanSpeed': <FanSpeed.Auto: 0>, 'airSwingHorizontal': <AirSwingLR.Mid: 2>, 'airSwingVertical': <AirSwingUD.Mid: 2>, 'eco': <EcoMode.Auto: 0>, 'nanoe': <NanoeMode.On: 2>}}
	return device 

def store_info():
	#json_str="{'id': '59a0c60fb6604818a6e29f1aa72d92be', 'parameters': {'temperatureInside': 22, 'temperatureOutside': 3, 'temperature': 21.0, 'power': <Power.On: 1>, 'mode': <OperationMode.Heat: 3>, 'fanSpeed': <FanSpeed.Auto: 0>, 'airSwingHorizontal': <AirSwingLR.Mid: 2>, 'airSwingVertical': <AirSwingUD.Mid: 2>, 'eco': <EcoMode.Auto: 0>, 'nanoe': <NanoeMode.On: 2>}}"
	info = get_info()
	#json_str = json_str.replace('\'', '"')
	#json_str = json_str.replace('<', '"')
	#json_str = json_str.replace('>', '"')
	#info = json.loads(json_str)
	#print(info['id'])
	#print(info['parameters']['temperatureInside'])
	temperatureInside = float(info['parameters']['temperatureInside'])
	temperatureOutside = float(info['parameters']['temperatureOutside'])
	temperature = float(info['parameters']['temperature'])
	
	kratoslib.writeTimeseriesData('panasonic.temperatureInside', temperatureInside)
	kratoslib.writeTimeseriesData('panasonic.temperatureOutside', temperatureOutside)
	kratoslib.writeTimeseriesData('panasonic.temperature', temperature)


def main(args):
	if len(args) == 0:
		print('USAGE: panasonic_control.py getinfo | storeinfo')
		exit(1)

	if args[0] == 'getinfo':
		device = get_info()
		print(device)

	if args[0] == 'storeinfo':
		store_info()

if __name__ == "__main__":
	config = ConfigObj(kratoslib.getKratosConfigFilePath('pcomfortcloud.conf'))
	main(sys.argv[1:])

