import requests
import urllib

import kratoslib
import json 


class easee_api:
	def __easee_request(self, method, url, payload=''):
		headers = {
			"Accept": "application/json",
			"Authorization": "Bearer " + kratoslib.readKratosConfigData('easee.accessToken')
		}
		response = requests.request(method, url, headers=headers, data=payload)
		if response.status_code == 200 or response.status_code == 202:
			return response
		if response.status_code == 402 or response.status_code == 404:
			self.__refreshToken()
			headers = {
				"Accept": "application/json",
				"Authorization": "Bearer " + kratoslib.readKratosConfigData('easee.accessToken')
			}
			response = requests.request(method, url, headers=headers, data=payload)
			if response.status_code == 200:
				return response
			else:
				print('Unable to request after refreshing token')
				return response
		else:
			print('Unknown response: ' + str(response.status_code))
			return response



	def __refreshToken(self):
		url = "https://api.easee.cloud/api/accounts/refresh_token"
		payload = '{"accesstoken":"' + kratoslib.readKratosConfigData('easee.accessToken') + '","refreshtoken":"' + kratoslib.readKratosConfigData('easee.refreshToken')  + '"}'
		headers = {
			"Accept": "application/json",
			"Authorization": "Bearer " + kratoslib.readKratosConfigData('easee.accessToken')
		}
		response=requests.post(url, data=payload, headers=headers)
		data=response.json()
		newAccessToken=data['accessToken']
		newRefreshToken=data['refreshToken']

		kratoslib.writeKratosConfigData('easee.accessToken', newAccessToken)
		kratoslib.writeKratosConfigData('easee.refreshToken', newRefreshToken)

		return 


	def printChargers(self):
		url = "https://api.easee.cloud/api/chargers"
		response = self.__easee_request("GET", url)

		for charger in response.json():
			print(charger['id'], charger['name'])
		
		return

	
	def printCharger(self, chargerId):
		url = f"https://api.easee.cloud/api/chargers/{chargerId}/details"
		response = self.__easee_request("GET", url)
		print(response.json())
	

	def printSite(self, chargerId):
		url = f"https://api.easee.cloud/api/chargers/{chargerId}/site"
		response = self.__easee_request("GET", url)
		print(response.json())


	def printConfig(self, chargerId):
		url = f"https://api.easee.cloud/api/chargers/{chargerId}/config"
		response = self.__easee_request("GET", url)
		print(response.json())


	def printWeeklyChargePlan(self, chargerId):
		url = f"https://api.easee.cloud/api/chargers/{chargerId}/weekly_charge_plan"
		response = self.__easee_request("GET", url)
		print(response.json())

	
	def printBasicChargePlan(self, chargerId):
		url = f"https://api.easee.cloud/api/chargers/{chargerId}/basic_charge_plan"
		response = self.__easee_request("GET", url)
		print(response.json())


	def setBasicChargePlan(self, chargerId, startTime):
		url = f"https://api.easee.cloud/api/chargers/{chargerId}/basic_charge_plan"
		payload = "{\"chargingCurrentLimit\":32,\"id\":\"" + chargerId + "\",\"chargeStartTime\":\"" + startTime + "\",\"repeat\":false,\"isEnabled\":true}"
		response = self.__easee_request("POST", url, payload)
		return (response.status_code == 202)


	def pauseCharging(self, chargerId):
		url = f"https://api.easee.cloud/api/chargers/{chargerId}/commands/pause_charging"
		response = self.__easee_request("POST", url)



	def resumeCharging(self, chargerId):
		url = f"https://api.easee.cloud/api/chargers/{chargerId}/commands/pause_charging"
		response = self.__easee_request("POST", url)



# Code to test the API
if __name__ == '__main__':	
	easee=easee_api()
	#easee.printChargers()
	#print(easee.setBasicChargePlan('EH562132', '2022-09-15T23:00:00Z'))
	easee.printBasicChargePlan('EH562132')
	#easee.printConfig('EH562132')


