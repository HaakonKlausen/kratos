#!/usr/bin/python3
# -*- coding: utf-8 -*-

# Based upon code copied from rewrite of ldtool
# Copyright (c) 2020 Jim Augustsson

# Modifications
# Copyright (c) 2021 Håkon Klausen

from configobj import ConfigObj
import getopt
import datetime
import sys
import json
import os
import pytz
import requests
from requests_oauthlib import OAuth1 as oauth
from urllib.parse import parse_qs

import kratoslib

PUBLIC_KEY = ''
PRIVATE_KEY = ''

TELLSTICK_TURNON = 1
TELLSTICK_TURNOFF = 2
TELLSTICK_BELL = 4
TELLSTICK_DIM = 16
TELLSTICK_UP = 128
TELLSTICK_DOWN = 256

SUPPORTED_METHODS = TELLSTICK_TURNON | TELLSTICK_TURNOFF | TELLSTICK_BELL | TELLSTICK_DIM | TELLSTICK_UP | TELLSTICK_DOWN;

def printUsage():
	print("Usage: %s [ options ]" % sys.argv[0])
	print("")
	print("Options:")
	print("         -[lnfdbvh] [ --list ] [ --help ]")
	print("                      [ --on device ] [ --off device ] [ --bell device ]")
	print("                      [ --dimlevel level --dim device ]")
	print("                      [ --up device --down device ]")
	print("")
	print("       --list (-l short option)")
	print("             List currently configured devices.")
	print("")
	print("       --help (-h short option)")
	print("             Shows this screen.")
	print("")
	print("       --on device (-n short option)")
	print("             Turns on device. 'device' must be an integer of the device-id")
	print("             Device-id and name is outputed with the --list option")
	print("")
	print("       --off device (-f short option)")
	print("             Turns off device. 'device' must be an integer of the device-id")
	print("             Device-id and name is outputed with the --list option")
	print("")
	print("       --dim device (-d short option)")
	print("             Dims device. 'device' must be an integer of the device-id")
	print("             Device-id and name is outputed with the --list option")
	print("             Note: The dimlevel parameter must be set before using this option.")
	print("")
	print("       --dimlevel level (-v short option)")
	print("             Set dim level. 'level' should an integer, 0-255.")
	print("             Note: This parameter must be set before using dim.")
	print("")
	print("       --bell device (-b short option)")
	print("             Sends bell command to devices supporting this. 'device' must")
	print("             be an integer of the device-id")
	print("             Device-id and name is outputed with the --list option")
	print("")
	print("       --up device")
	print("             Sends up command to devices supporting this. 'device' must")
	print("             be an integer of the device-id")
	print("             Device-id and name is outputed with the --list option")
	print("")
	print("       --down device")
	print("             Sends down command to devices supporting this. 'device' must")
	print("             be an integer of the device-id")
	print("             Device-id and name is outputed with the --list option")
	print("")
	print("Report bugs to <info.tech@telldus.se>")

def listDevices():
	response = doRequest('devices/list', {'supportedMethods': SUPPORTED_METHODS})
	print("Number of devices: %i" % len(response['device']));
	for device in response['device']:
		if (device['state'] == TELLSTICK_TURNON):
			state = 'ON'
		elif (device['state'] == TELLSTICK_TURNOFF):
			state = 'OFF'
		elif (device['state'] == TELLSTICK_DIM):
			state = "DIMMED"
		elif (device['state'] == TELLSTICK_UP):
			state = "UP"
		elif (device['state'] == TELLSTICK_DOWN):
			state = "DOWN"
		else:
			state = 'Unknown state'

		print("%s\t%s\t%s" % (device['id'], device['name'], state))

def listSensors():
    response = doRequest('sensors/list', {'supportedMethods': SUPPORTED_METHODS})
    for sensor in response['sensor']:
        print("%s\t%s" % (sensor['id'], sensor['name']))

def sensorInfo(sensorId):
    response = doRequest('sensor/info', {'id': sensorId})
    print(response)
    print(response['name'])
    for data in response['data']:
        print("\t%s\t%s" % (data['name'], data['value']))

def getSensorInfo(sensorId, name1, name2):
    response = doRequest('sensor/info', {'id': sensorId})
    value1 = 0
    value2 = 0
    for data in response['data']:
        if data['name'] == name1:
            value1 = data['value']
        if data['name'] == name2:
            value2 = data['value']
    return value1, value2


# Works on the assumption that we sample 6 times an hour.  
# Could be improved by using time limits instead.

def calculateAverages():
	connection=kratoslib.getConnection()
	sql = ("select value from timeseries where seriesname = 'in.temp' order by created desc limit 24")
	sum60 = 0.0
	sum120 = 0.0
	sum240 = 0.0
	count = 0
	cursor=connection.cursor()
	cursor.execute(sql)
	for value in cursor:
		if count < 6:
			sum60 = sum60 + value[0]
		if count < 12:
			sum120 = sum120 + value[0]
		sum240 = sum240 + value[0]
		count = count + 1
	cursor.close()
	connection.close()

	average60min = float(sum60/6)
	average120min = float(sum120/12)
	average240min = float(sum240/24)

	return average60min, average120min, average240min


def kratosData():
    # Get temp and humidity for in and out
    # Out sensor ID 1547679697 (Vedbod)
    # In  sensor ID 1548595445 (Hjemmekontor)
	kratoslib.writeKratosLog('DEBUG', 'Collencting Telldus sensors info')

	in_temp, in_humidity = getSensorInfo('1548595445', 'temp', 'humidity')
	out_temp, out_humidity = getSensorInfo('1547679697', 'temp', 'humidity')
    
	now=datetime.datetime.now(pytz.utc)

	kratoslib.writeKratosData("in.temp", in_temp)
	kratoslib.writeKratosData("in.humidity", in_humidity)
	kratoslib.writeKratosData("out.temp", out_temp)
	kratoslib.writeKratosData("out.humidity", out_humidity)

	kratoslib.writeTimeseriesDataTime("in.temp", in_temp, now)
	kratoslib.writeTimeseriesDataTime("in.humidity", in_humidity, now)
	kratoslib.writeTimeseriesDataTime("out.temp", out_temp, now)
	kratoslib.writeTimeseriesDataTime("out.humidity", out_humidity, now)

	#average60min = str(round(calculateAverage60min(), 1))
	#print(average60min)
	#kratoslib.writeTimeseriesDataTime("in.temp.avg60min", average60min, now)
	#kratoslib.writeKratosData("in.temp.avg60min", average60min)

	average60min, average120min, average240min = calculateAverages()
	kratoslib.writeTimeseriesDataTime("in.temp.avg60min", average60min, now)
	kratoslib.writeTimeseriesDataTime("in.temp.avg120min", average120min, now)
	kratoslib.writeTimeseriesDataTime("in.temp.avg240min", average240min, now)

	in_temp, in_humidity = getSensorInfo('1554261662', 'temp', 'humidity')
	out_temp, out_humidity = getSensorInfo('1554261686', 'temp', 'humidity')

	kratoslib.writeTimeseriesDataTime("hytten.in.temp", in_temp, now)
	kratoslib.writeTimeseriesDataTime("hytten.in.humidity", in_humidity, now)
	#kratoslib.writeTimeseriesDataTime("hytten.out.temp", out_temp, now)
	kratoslib.writeTimeseriesDataTime("hytten.out_kjokken.temp", out_temp, now)

	out_temp, out_humidity = getSensorInfo('1555014559', 'temp', 'humidity')
	kratoslib.writeTimeseriesDataTime("hytten.out.temp", out_temp, now)
	kratoslib.writeTimeseriesDataTime("hytten.out.humidity", out_humidity, now)

	bad_temp, bad_humidity = getSensorInfo('1554261848', 'temp', 'humidity')
	stue_temp, stue_humidity = getSensorInfo('1554261980', 'temp', 'humidity')

	kratoslib.writeTimeseriesDataTime("hytten.bad.temp", bad_temp, now)
	kratoslib.writeTimeseriesDataTime("hytten.bad.humidity", bad_humidity, now)
	kratoslib.writeTimeseriesDataTime("hytten.stue.temp", stue_temp, now)
	kratoslib.writeTimeseriesDataTime("hytten.stue.humidity", stue_humidity, now)


def doMethod(deviceId, methodId, methodValue = 0):
	response = doRequest('device/info', {'id': deviceId})

	if (methodId == TELLSTICK_TURNON):
		method = 'on'
	elif (methodId == TELLSTICK_TURNOFF):
		method = 'off'
	elif (methodId == TELLSTICK_BELL):
		method = 'bell'
	elif (methodId == TELLSTICK_UP):
		method = 'up'
	elif (methodId == TELLSTICK_DOWN):
		method = 'down'

	if ('error' in response):
		name = ''
		retString = response['error']
	else:
		name = response['name']
		response = doRequest('device/command', {'id': deviceId, 'method': methodId, 'value': methodValue})
		if ('error' in response):
			retString = response['error']
		else:
			retString = response['status']

	if (methodId in (TELLSTICK_TURNON, TELLSTICK_TURNOFF)):
		print("Turning %s device %s, %s - %s" % ( method, deviceId, name, retString));
	elif (methodId in (TELLSTICK_BELL, TELLSTICK_UP, TELLSTICK_DOWN)):
		print("Sending %s to: %s %s - %s" % (method, deviceId, name, retString))
	elif (methodId == TELLSTICK_DIM):
		print("Dimming device: %s %s to %s - %s" % (deviceId, name, methodValue, retString))


def doRequest(method, params):
	global config
	consumer = oauth(config['publicKey'], client_secret=config['privateKey'], resource_owner_key=config['token'], resource_owner_secret=config['tokenSecret'])
	response = requests.post(url="http://api.telldus.com/json/" + method, data=params, auth=consumer)
	return json.loads(response.content.decode('utf-8'))

def requestToken():
	global config
	consumer = oauth(PUBLIC_KEY, client_secret=PRIVATE_KEY, resource_owner_key=None, resource_owner_secret=None)
	request = requests.post(url='http://api.telldus.com/oauth/requestToken', auth=consumer)
	credentials = parse_qs(request.content.decode('utf-8'))
	key = credentials.get('oauth_token')[0]
	token = credentials.get('oauth_token_secret')[0]
	print('Open the following url in your webbrowser:\nhttp://api.telldus.com/oauth/authorize?oauth_token=%s\n' % key)
	print('After logging in and accepting to use this application run:\n%s --authenticate' % (sys.argv[0]))
	config['requestToken'] = str(key)
	config['requestTokenSecret'] = str(token)
	saveConfig()

def getAccessToken():
	global config
	consumer = oauth(PUBLIC_KEY, client_secret=PRIVATE_KEY, resource_owner_key=config['requestToken'], resource_owner_secret=config['requestTokenSecret'])
	request = requests.post(url='http://api.telldus.com/oauth/accessToken', auth=consumer)
	credentials = parse_qs(request.content.decode('utf-8'))
	if request.status_code != 200:
		print('Error retreiving access token, the server replied:\n%s' %request.content)
		return
	token = credentials.get('oauth_token_secret')[0]
	config['requestToken'] = None
	config['requestTokenSecret'] = None
	config['token'] = str(credentials.get('oauth_token')[0])
	config['tokenSecret'] = str(token)
	print('Authentication successful, you can now use tdtool')
	saveConfig()

def authenticate():
	try:
		opts, args = getopt.getopt(sys.argv[1:], '', ['authenticate'])
		for opt, arg in opts:
			if opt in ('--authenticate'):
				getAccessToken()
				return
	except getopt.GetoptError:
		pass
	requestToken()

def saveConfig():
	global config
	try:
		os.makedirs(os.path.expanduser('~') + '/.config/Telldus')
	except:
		pass
	config.write()

def main(argv):
	global config
	if ('token' not in config or config['token'] == ''):
		authenticate()
		return
	try:
		opts, args = getopt.getopt(argv, "ln:f:d:b:v:h:s:k:-", ["list", "listsensors", "kratosdata", "sensorinfo=", "on=", "off=", "dim=", "bell=", "dimlevel=", "up=", "down=", "help"])
	except getopt.GetoptError:
		printUsage()
		sys.exit(2)

	dimlevel = -1

	for opt, arg in opts:
		if opt in ("-h", "--help"):
			printUsage()

		elif opt in ("-l", "--list"):
			listDevices()

		elif opt in ("-s", "--listsensors"):
			listSensors()

		elif opt in ("-n", "--on"):
			doMethod(arg, TELLSTICK_TURNON)

		elif opt in ("-f", "--off"):
			doMethod(arg, TELLSTICK_TURNOFF)

		elif opt in ("-i", "--sensorinfo"):
			sensorInfo(arg)

		elif opt in ("-k", "--kratosdata"):
			kratosData()

		elif opt in ("-b", "--bell"):
			doMethod(arg, TELLSTICK_BELL)

		elif opt in ("-d", "--dim"):
			if (dimlevel < 0):
				print("Dimlevel must be set with --dimlevel before --dim")
			else:
				doMethod(arg, TELLSTICK_DIM, dimlevel)

		elif opt in ("-v", "--dimlevel"):
			dimlevel = int(arg)

		elif opt in ("--up"):
			doMethod(arg, TELLSTICK_UP)

		elif opt in ("--down"):
			doMethod(arg, TELLSTICK_DOWN)

if __name__ == "__main__":
	config = ConfigObj(kratoslib.getKratosConfigFilePath('tdtool.conf'))
	main(sys.argv[1:])