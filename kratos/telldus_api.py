from tkinter.tix import TCL_ALL_EVENTS
from configobj import ConfigObj
import json
import requests
from requests_oauthlib import OAuth1 as oauth
from urllib.parse import parse_qs

import constants
import kratoslib

TELLSTICK_TURNON = 1
TELLSTICK_TURNOFF = 2
TELLSTICK_BELL = 4
TELLSTICK_DIM = 16
TELLSTICK_UP = 128
TELLSTICK_DOWN = 256

SUPPORTED_METHODS = TELLSTICK_TURNON | TELLSTICK_TURNOFF | TELLSTICK_BELL | TELLSTICK_DIM | TELLSTICK_UP | TELLSTICK_DOWN

class telldus_api:
	def __init__(self):
		self.config = ConfigObj(kratoslib.getKratosConfigFilePath('tdtool.conf'))

	def __doMethod(self, deviceId, methodId, methodValue = 0):
		response = self.__doRequest('device/info', {'id': deviceId})

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
			response = self.__doRequest('device/command', {'id': deviceId, 'method': methodId, 'value': methodValue})
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


	def __doRequest(self, method, params):
		consumer = oauth(self.config['publicKey'], client_secret=self.config['privateKey'], resource_owner_key=self.config['token'], resource_owner_secret=self.config['tokenSecret'])
		response = requests.post(url="http://api.telldus.com/json/" + method, data=params, auth=consumer)
		return json.loads(response.content.decode('utf-8'))

	def __requestToken(self):
		consumer = oauth(PUBLIC_KEY, client_secret=PRIVATE_KEY, resource_owner_key=None, resource_owner_secret=None)
		request = requests.post(url='http://api.telldus.com/oauth/requestToken', auth=consumer)
		credentials = parse_qs(request.content.decode('utf-8'))
		key = credentials.get('oauth_token')[0]
		token = credentials.get('oauth_token_secret')[0]
		print('Open the following url in your webbrowser:\nhttp://api.telldus.com/oauth/authorize?oauth_token=%s\n' % key)
		print('After logging in and accepting to use this application run:\n%s --authenticate' % (sys.argv[0]))
		self.config['requestToken'] = str(key)
		self.config['requestTokenSecret'] = str(token)
		__saveConfig()

	def __getAccessToken(self):
		consumer = oauth(PUBLIC_KEY, client_secret=PRIVATE_KEY, resource_owner_key=self.config['requestToken'], resource_owner_secret=self.config['requestTokenSecret'])
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

	def __authenticate(self):
		try:
			opts, args = getopt.getopt(sys.argv[1:], '', ['authenticate'])
			for opt, arg in opts:
				if opt in ('--authenticate'):
					self.__getAccessToken()
					return
		except getopt.GetoptError:
			pass
		self.__requestToken()

	def __saveConfig(self):
		try:
			os.makedirs(os.path.expanduser('~') + '/.config/Telldus')
		except:
			pass
		self.config.write()

	def getDevices(self):
		response = self.__doRequest('devices/list', {'supportedMethods': SUPPORTED_METHODS})
		return response

	def getSensors(self):
		response = self.__doRequest('sensors/list', {'supportedMethods': SUPPORTED_METHODS})
		return response


	# Update the telldusdevices table with 
	def updateDatabase(self):
		response = self.getDevices()
	
	def turnOn(self, deviceId):
		self.__doMethod(deviceId, TELLSTICK_TURNON)

	def turnOff(self, deviceId):
		self.__doMethod(deviceId, TELLSTICK_TURNOFF)


	def getSensorInfo(self, sensorId, name1, name2):
		response = self.__doRequest('sensor/info', {'id': sensorId})
		value1 = 0
		value2 = 0
		for data in response['data']:
			if data['name'] == name1:
				value1 = data['value']
			if data['name'] == name2:
				value2 = data['value']
		return value1, value2


def listDevices(telldus_api):
	response = telldus_api.getDevices()
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

if __name__ == "__main__":

	def listSensors(telldus_api):
		response = telldus_api.getSensors()
		print("Number of sensors: %i" % len(response['sensor']));
		for sensor in response['sensor']:
			print("%s\t%s" % (sensor['id'], sensor['name']))


	def getCottageKitchenTemp(telldus_api):
		return telldus_api.getSensorInfo(constants.BjonntjonnKitchenInTemp, 'temp', 'humidity')

	def getHomeKitchenTemp(telldus_api):
		return telldus_api.getSensorInfo(constants.OdderheiKitchenInTemp, 'temp', 'humidity')


	telldus_api = telldus_api()
	listDevices(telldus_api)
	listSensors(telldus_api)
	
	print(f"Bjønntjonn temp: {getCottageKitchenTemp(telldus_api)}")
	print(f"Odderhei temp: {getHomeKitchenTemp(telldus_api)}")