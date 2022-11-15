#!/usr/bin/python3
#
# Control the power usage and temperature of the Panasonic air-to-air heater
#
import argparse
from configobj import ConfigObj
import datetime
import pytz
import json
import sys
import time

import pcomfortcloud

import constants
import kratoslib


class PanasonicApi:
	def __init__(self):
		self.__config = ConfigObj(kratoslib.getKratosConfigFilePath('pcomfortcloud.conf'))
		self.__session = self.__get_session()
		self.__id = self.__get_id()


	def __get_session(self):
		try:
			user=self.__config['user']
			password=self.__config['password']
			session = pcomfortcloud.Session(user, password, tokenFileName='/home/pi/.panasonic-token')
			session.login()
			return session
		except Exception as e:
			kratoslib.writeKratosLog('ERROR', 'Unable to create pcomfortcloud sesseion: ' + str(e))
			#print(f"Error in getting session: {e}")
			exit(1)

	def __get_id(self):
		try:
			devices = self.__session.get_devices()
		except Exception as e:
			kratoslib.writeKratosLog('ERROR', 'Error in getting devices')
			print('Error in getting devices' + str(e))
			exit(1)

		id=devices[0]['id']
		return id

	def get_hourly_power_consumption(self, datestr):
		consumption=[]
		try:
			history = self.__session.history(self.__id, 'Day', datestr)
			for historyData in history['parameters']['historyDataList']:
				hour_consumption={"hour": historyData['dataNumber'], "consumption": historyData ['consumption']}
				consumption.append(hour_consumption)
			return consumption 

		except Exception as e:
			kratoslib.writeKratosLog('ERROR', 'Error in getting history info')
			print('Error in getting device info' + str(e))
			exit(1)

	def get_info(self):
		try:
			device_info=self.__session.get_device(self.__id)
		except Exception as e:
			kratoslib.writeKratosLog('ERROR', 'Error in getting device info')
			print('Error in getting device info' + str(e))
			exit(1)

		#print(device)
		# {'id': '59a0c60fb6604818a6e29f1aa72d92be', 'parameters': 
		# 	{'temperatureInside': 22, 'temperatureOutside': 3, 'temperature': 21.0, 'power': <Power.On: 1>, 'mode': <OperationMode.Heat: 3>, 'fanSpeed': <FanSpeed.Auto: 0>, 'airSwingHorizontal': <AirSwingLR.Mid: 2>, 'airSwingVertical': <AirSwingUD.Mid: 2>, 'eco': <EcoMode.Auto: 0>, 'nanoe': <NanoeMode.On: 2>}}
		return device_info

	def get_power_temperature(self):
		device_info = self.get_info()

		power_str=str(device_info['parameters']['power'])
		if power_str == 'Power.On':
			power=constants.Power.On
		else:
			power=constants.Power.Off
		temperature=device_info['parameters']['temperature']
		return power, temperature

	def set_temperature(self, new_temperature):
		print("Setting temperature")
		self.__session.set_device(self.__id, temperature=new_temperature, fanSpeed=pcomfortcloud.constants.FanSpeed.High, eco=pcomfortcloud.constants.EcoMode.Auto, airSwingVertical=pcomfortcloud.constants.AirSwingUD.UpMid, airSwingHorizontal=pcomfortcloud.constants.AirSwingLR.Mid)

	def set_temperatureLowFan(self, new_temperature):
		print("Setting LowFan Temp")
		self.__session.set_device(self.__id, temperature=new_temperature, fanSpeed=pcomfortcloud.constants.FanSpeed.Low, eco=pcomfortcloud.constants.EcoMode.Quiet, airSwingVertical=pcomfortcloud.constants.AirSwingUD.Down, airSwingHorizontal=pcomfortcloud.constants.AirSwingLR.Left)

	def poweron(self):
		self.__session.set_device(self.__id, power=pcomfortcloud.constants.Power.On)

	def poweroff(self):
		self.__session.set_device(self.__id, power=pcomfortcloud.constants.Power.Off)

	def set_fanspeedHigh(self):
		self.__session.set_device(self.__id, fanSpeed=pcomfortcloud.constants.FanSpeed.High)

	def set_fanspeedAuto(self):
		self.__session.set_device(self.__id, fanSpeed=pcomfortcloud.constants.FanSpeed.Auto)

	def set_fanspeedLow(self):
		self.__session.set_device(self.__id, fanSpeed=pcomfortcloud.constants.FanSpeed.Low)

	def set_default(self):
		self.__session.set_device(self.__id, fanSpeed=pcomfortcloud.constants.FanSpeed.Auto , mode=pcomfortcloud.constants.OperationMode.Heat, eco=pcomfortcloud.constants.EcoMode.Auto, airSwingVertical=pcomfortcloud.constants.AirSwingUD.UpMid, airSwingHorizontal=pcomfortcloud.constants.AirSwingLR.Auto)


def main():
	parser = argparse.ArgumentParser()
	parser.add_argument("command", type=str, help="settemp --temperature N | poweron | poweroff | getinfo | getpower")
	parser.add_argument("--temperature", type=int, required=False)
	args = parser.parse_args()
	if args.command == "settemp":
		if not args.temperature:
			print ("Missing required argument: --temperature")
			exit (-1)
		panasonic_api = PanasonicApi()
		panasonic_api.set_temperature(args.temperature)

	elif args.command == "poweron":
		panasonic_api = PanasonicApi()
		panasonic_api.poweron()
		print("Power On")
	elif args.command == "poweroff":
		panasonic_api = PanasonicApi()
		panasonic_api.poweroff()
		print("Power Off")
	elif args.command == "getinfo":
		panasonic_api = PanasonicApi()
		device_info = panasonic_api.get_info()
		print(device_info)
	elif args.command == "getpower":
		panasonic_api = PanasonicApi()
		power, temperature = panasonic_api.get_power_temperature()
		print (power, temperature)
	elif args.command == "set_default":
		panasonic_api = PanasonicApi()
		panasonic_api.set_default()
	else:
		print("Unknown command")


if __name__ == "__main__":
	#main(sys.argv[1:])
	main()

