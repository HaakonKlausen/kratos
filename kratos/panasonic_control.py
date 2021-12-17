#!/usr/bin/python3
#
# Control the power usage and temperature of the Panasonic air-to-air heater
#
import sys
from configobj import ConfigObj

import pcomfortcloud
import kratoslib

def get_session():
	global config

	try:
		user=''
		password=''
		session = pcomfortcloud.Session(user, password)
		session.login()
		return session
	except Exception as e:
		print('Error in login: ' + str(e))
		exit(1)

def get_info():
	session = get_session()
	#devices = session.get_devices()
	#print(devices)
	# [{'id': '59a0c60fb6604818a6e29f1aa72d92be', 'name': 'Stue', 'group': 'My House', 'model': ''}]
	id=config['id']
	print(id)
	device=session.get_device(id)
	print(device)
	# {'id': '59a0c60fb6604818a6e29f1aa72d92be', 'parameters': 
	# 	{'temperatureInside': 22, 'temperatureOutside': 3, 'temperature': 21.0, 'power': <Power.On: 1>, 'mode': <OperationMode.Heat: 3>, 'fanSpeed': <FanSpeed.Auto: 0>, 'airSwingHorizontal': <AirSwingLR.Mid: 2>, 'airSwingVertical': <AirSwingUD.Mid: 2>, 'eco': <EcoMode.Auto: 0>, 'nanoe': <NanoeMode.On: 2>}}

def store_info():
	json_str="{'id': '59a0c60fb6604818a6e29f1aa72d92be', 'parameters': {'temperatureInside': 22, 'temperatureOutside': 3, 'temperature': 21.0, 'power': <Power.On: 1>, 'mode': <OperationMode.Heat: 3>, 'fanSpeed': <FanSpeed.Auto: 0>, 'airSwingHorizontal': <AirSwingLR.Mid: 2>, 'airSwingVertical': <AirSwingUD.Mid: 2>, 'eco': <EcoMode.Auto: 0>, 'nanoe': <NanoeMode.On: 2>}}"

def main(args):
	if len(args) == 0:
		print('USAGE: panasonic_control.py getinfo | storeinfo')
		exit(1)

	if args[0] == 'getinfo':
		get_info()

if __name__ == "__main__":
	config = ConfigObj(kratoslib.getKratosConfigFilePath('pcomfortcloud.conf'))
	main(sys.argv[1:])

