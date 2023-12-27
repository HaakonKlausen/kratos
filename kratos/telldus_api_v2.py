import datetime
import requests
from configobj import ConfigObj
from requests_oauthlib import OAuth1 as oauth
import time
import json
import kratoslib

BASE_URL = "https://pa-api.telldus.com"
TELLSTICK_TURNON = 1
TELLSTICK_TURNOFF = 2
TELLSTICK_BELL = 4
TELLSTICK_DIM = 16
TELLSTICK_UP = 128
TELLSTICK_DOWN = 256

SUPPORTED_METHODS = TELLSTICK_TURNON | TELLSTICK_TURNOFF | TELLSTICK_BELL | TELLSTICK_DIM | TELLSTICK_UP | TELLSTICK_DOWN

class TelldusApi():
    def __init__(self):
        self.__config = ConfigObj(kratoslib.getKratosConfigFilePath('tdtool.conf'))
        self.__publicKey = self.__config['publicKey']
        self.__privateKey = self.__config['privateKey']
        self.__token = self.__config['token']
        self.__secret = self.__config['tokenSecret']

        self.__consumer = oauth(client_key=self.__publicKey, client_secret=self.__privateKey, resource_owner_key=self.__token, resource_owner_secret=self.__secret)

    def list_devices(self):
        url = f"{BASE_URL}/json/devices/list"
        print(url)
        response = requests.get(url=url, auth=self.__consumer, params={'supportedMethods': SUPPORTED_METHODS})
        print("Waiting...")
        time.sleep(10)
        response_json = json.loads(response.text)
        response_json_formatted = json.dumps(response_json, indent=4, sort_keys=True)  
        print(response_json_formatted)

    def list_sensors(self):
        url = f"{BASE_URL}/json/sensors/list"
        print(url)
        response = requests.get(url=url, auth=self.__consumer, params={'supportedMethods': SUPPORTED_METHODS})
        print("Waiting...")
        time.sleep(10)
        response_json = json.loads(response.text)
        response_json_formatted = json.dumps(response_json, indent=4, sort_keys=True)  
        print(response_json_formatted)

    def getSensorInfoUpdated(self, sensorId, name1, name2):
        url = f"{BASE_URL}/json/sensor/info"
        response = requests.get(url=url, auth=self.__consumer, params= {'id': sensorId})
        print("Waiting...")
        time.sleep(10)
        if response.status_code != 200:
            print(f"Error: {response.status_code} - {response.text}")
            return None
        response_json = json.loads(response.text)
        response_json_formatted = json.dumps(response_json, indent=4, sort_keys=True)  
        #print(response_json_formatted)
        value1 = 0
        value2 = 0
        lastUpdatedTimestamp = 0
        if 'data' in response_json:
            for data in response_json['data']:
                if data['name'] == name1:
                    value1 = data['value']
                    lastUpdatedTimestamp = data['lastUpdated']
                if data['name'] == name2:
                    value2 = data['value']
        lastUpdated = datetime.datetime.fromtimestamp(lastUpdatedTimestamp)
        return value1, value2, lastUpdated

    def __doMethod(self, deviceId, methodId):
        command = ""
        if methodId == TELLSTICK_TURNON:
            command="turnOn"
        elif methodId == TELLSTICK_TURNOFF:
            command="turnOff"
        else:
            print(f"Error in __doMethod: Unsupported method {methodId}")
            return None
        url = f"{BASE_URL}/json/device/{command}"
        params = {'id': deviceId} 
        response = requests.get(url=url, auth=self.__consumer, params=params)
        print("Waiting...")
        time.sleep(15)
        if response.status_code != 200:
            print(f"Error in __doMethod: {response.status_code} - {response.text}")
    
    def turnOn(self, deviceId):
        self.__doMethod(deviceId, TELLSTICK_TURNON)

    def turnOff(self, deviceId):
        self.__doMethod(deviceId, TELLSTICK_TURNOFF)


if __name__ == "__main__":
    t = TelldusApi()
    #t.list_sensors()
    #temp, humidity, lastUpdated = t.getSensorInfoUpdated('1555014559', 'temp', 'humidity')
    #print(f"temp: {temp}, humidity: {humidity}, lastUpdated: {lastUpdated}")
    #t.list_devices()
    t.turnOff("11290926")