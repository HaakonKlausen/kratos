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

def log_info(on, targetTemperature, temperature, humidity):
	on_int = 0
	if on:
		on_int = 1
	kratoslib.writeTimeseriesData('sensibo.on', on_int)
	kratoslib.writeTimeseriesData('sensibo.temperatureOutside', temperature)
	kratoslib.writeTimeseriesData('sensibo.humidity', humidity)
	kratoslib.writeTimeseriesData('sensibo.targetTemperature', targetTemperature)

def main(args):
	kratoslib.writeKratosLog('DEBUG', 'Sensibo Control running')
	client = get_client()
	uid = get_uid(client)
	on, targetTemperature, temperature, humidity = get_info(client, uid)
	log_info(on, targetTemperature, temperature, humidity)



if __name__ == "__main__":
	config = ConfigObj(kratoslib.getKratosConfigFilePath('sensibo.conf'))
	main(sys.argv[1:])
