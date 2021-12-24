import requests
import urllib

import kratoslib

def easee_request(method, url, headers, params, payload=''):
	print(method, url, headers, payload)
	response = requests.request(method, url, headers=headers, data=payload)
	if response.status_code == 200:
		return response
	if response.status_code == 402 or response.status_code == 404:
		getRefreshToken()
		response = requests.request(method, url, headers=headers)
		if response.status_code == 200:
			return response
		else:
			print('Unable to request after refreshing token')
			return response
	else:
		print('Unknown response: ' + str(response.status_code))
		return response

def easee_tokenized_request(method, url, params, payload=''):

	headers = {
		"Accept": "application/json",
		"Content-Type": "application/*+json",
		"Authorization": "Bearer " + kratoslib.readKratosConfigData('easee.accessToken')
	}
	return easee_request(method, url, headers, params, payload=payload)


def getRefreshToken():
	url = "https://api.easee.cloud/api/accounts/refresh_token"
	payload = '{"accesstoken":"' + kratoslib.readKratosConfigData('easee.accessToken') + '","refreshtoken":"' + kratoslib.readKratosConfigData('easee.accessToken')  + '"}'
	#payload = {
	#	"accesstoken": kratoslib.readKratosConfigData('easee.accessToken'),
	#	"refreshtoken": kratoslib.readKratosConfigData('easee.accessToken')
	#}
	params = urllib.parse.urlencode({
	})
	response=easee_tokenized_request("POST", url, params, payload=payload)
	print(response.json())
	#payload = "{\"accessToken\":\"s\",\"refreshToken\":\"f\"}"
	return response

def getChargers():
	url = "https://api.easee.cloud/api/chargers"
	params = urllib.parse.urlencode({
	})
	return easee_tokenized_request("GET", url, params)
	


#response=getChargers()
response=getRefreshToken()
print(response.json())
print(response.status_code)


	#print(response.text)

