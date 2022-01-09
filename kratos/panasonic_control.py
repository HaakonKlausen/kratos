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
		kratoslib.writeKratosLog('ERROR', 'Unable to create pcomfortcloud sesseion: ' + str(e))
		exit(1)

def get_info():
	session = get_session()
	try:
		devices = session.get_devices()
	except Exception as e:
		kratoslib.writeKratosLog('ERROR', 'Error in getting devices')
		print('Error in getting devices' + str(e))
		exit(1)

	#print(devices)
	# [{'id': '59a0c60fb6604818a6e29f1aa72d92be', 'name': 'Stue', 'group': 'My House', 'model': ''}]
	id=devices[0]['id']
	#print(id)
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

def main(args):
	if len(args) == 0:
		print('USAGE: panasonic_control.py getinfo | storeinfo')
		exit(1)

	if args[0] == 'getinfo':
		info = get_info()
		print(info)
		print(info['parameters']['power'])

	if args[0] == 'storeinfo':
		info = get_info()
		store_info(info)

	

if __name__ == "__main__":
	config = ConfigObj(kratoslib.getKratosConfigFilePath('pcomfortcloud.conf'))
	main(sys.argv[1:])

