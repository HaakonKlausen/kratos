#!/usr/bin/python3

import sys
from configobj import ConfigObj
import json

import kratoslib
import sensibo_client

global config


def get_client():
	return sensibo_client.SensiboClientAPI(config['apikey'])

def get_uid(client):
	devices = client.devices()
	return devices[config['devicename']]

def get_info(client, uid):
	ac_state = client.pod_ac_state(uid)
	measurements = client.pod_measurement(uid)
	on = ac_state['on']
	targetTemperature = ac_state['targetTemperature']
	temperature = measurements[0]['temperature']
	humidity = measurements[0]['humidity']
	return on, targetTemperature, temperature, humidity

def set_targetTemperature(client, uid, new_targetTempearature):
	kratoslib.writeKratosLog('INFO', 'Setting new target temperature: ' + str(new_targetTempearature))
	print('Setting new target temperature: ' + str(new_targetTempearature))
	ac_state = client.pod_ac_state(uid)
	client.pod_change_ac_state(uid, ac_state, "targetTemperature", new_targetTempearature)
	kratoslib.writeKratosData('sensibo.targetTemperature', str(new_targetTempearature))

def power(client, uid, powerstate):
	ac_state = client.pod_ac_state(uid)
	client.pod_change_ac_state(uid, ac_state, "on", powerstate)
	powerstate_text = 'Av'
	if powerstate == True:
		powerstate_text = 'På'
	kratoslib.writeKratosData('sensibo.powerstate', powerstate_text)
	kratoslib.writeKratosLog('INFO', 'Changing powerstate to ' + powerstate_text)

def log_info(on, targetTemperature, temperature, humidity):
	on_int = 0
	if on:
		on_int = 1
	kratoslib.writeTimeseriesData('sensibo.on', on_int)
	kratoslib.writeTimeseriesData('sensibo.temperatureOutside', temperature)
	kratoslib.writeTimeseriesData('sensibo.humidity', humidity)
	kratoslib.writeTimeseriesData('sensibo.targetTemperature', targetTemperature)

	kratoslib.writeKratosData('sensibo.targetTemperature', str(targetTemperature))

def calculate_new_target(in_temperature, targetTemperature, desiredTemperature=20, defaultDesiredOffset=0):
	new_targetTempearature = targetTemperature
	if in_temperature >= 20.8:
		new_targetTempearature = 18
	elif in_temperature >= 20.5:
		new_targetTempearature = 19
	elif in_temperature < 19.8:
		new_targetTempearature = 20
	elif in_temperature <=19.5:
		new_targetTempearature = 21
	elif in_temperature < 19.0:
		new_targetTempearature = 22

	#diff_temp = int(round(float(in_temperature), 0) - float(desiredTemperature))
	#print(targetTemperature,  diff_temp)
	#additionalOffset=int(round(in_temperature, 0)) - desiredTemperature
	#new_targetTempearature = int(desiredTemperature) - defaultDesiredOffset - additionalOffset



	# Safety boundaries
	if new_targetTempearature < 18:
		new_targetTempearature = 18
	elif new_targetTempearature > 22:
		new_targetTempearature = 22

	#new_targetTempearature = 20

	return new_targetTempearature


	
def main(args):
	# Connect
	kratoslib.writeKratosLog('DEBUG', 'Sensibo Control running')
	client = get_client()
	uid = get_uid(client)

	# Get and log basic info
	on, targetTemperature, temperature, humidity = get_info(client, uid)
	log_info(on, targetTemperature, temperature, humidity)
	# Check if we need to adjust target temperature
	in_temperature = float(kratoslib.readKratosData('in.temp'))
	if len(args) == 1:
		if args[0] == 'adjust':
			if on == True:
				desiredTemperature = int(config['desiredTemperature'])
				defaultDesiredOffset = int(config['defaultDesiredOffset'])
				new_targetTempearature = calculate_new_target(	in_temperature, targetTemperature, 
																desiredTemperature=desiredTemperature, defaultDesiredOffset=defaultDesiredOffset)
				if new_targetTempearature != targetTemperature:
					set_targetTemperature(client, uid, new_targetTempearature)
				if kratoslib.readKratosData('yr.symbol_code') == 'clearsky_day' and in_temperature >= 20.0:
					power(client, uid, False)
			else:
				if kratoslib.readKratosData('yr.symbol_code') != 'clearsky_day' or in_temperature < 19.5:
					power(client, uid, True)

		if args[0] == 'poweron':
			power(client, uid, True)

		if args[0] == 'poweroff':
			power(client, uid, False)

if __name__ == "__main__":
	config = ConfigObj(kratoslib.getKratosConfigFilePath('sensibo.conf'))
	main(sys.argv[1:])
