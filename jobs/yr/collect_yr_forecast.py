import sys
import getopt
import os
import json
import requests
from requests_oauthlib import OAuth1 as oauth
from configobj import ConfigObj
import http.client, urllib.request, urllib.parse, urllib.error, base64


def get_yr_data():
	global config 

	headers = {
		# Request headers
		'User-Agent': 'Kratos/0.1 hakon.klausen@icloud.com',
	}


	params = urllib.parse.urlencode({
	})

	try:
		conn = http.client.HTTPSConnection('api.met.no')
		conn.request("GET", "/weatherapi/locationforecast/2.0/compact?altitude=0&lat=58.14&lon=7.99&%s" % params, "{body}", headers)
		response = conn.getresponse()
		data = response.read()
		print(data)
		conn.close()
	except Exception as e:
		print("[Errno {0}] {1}".format(e.errno, e.strerror))

	return json.loads(data.decode('utf-8'))


def parse_yr_data(yr_data):
	antall_innlagte_sshf = '0'
	antall_innlagte_foretak = '0'
	totalt_innlagte = 0
	dato_oppdatert = ''
	for foretak in covid_data:
		foretak_name = foretak['helseforetakNavn']
		#print(foretak_name)
		if foretak_name == 'Sørlandet sykehus HF':
			for registrering in foretak['covidRegistreringer']:
				#print("\t%s\t%s" % (registrering['dato'], registrering['antInnlagte']))
				antall_innlagte_sshf = registrering['antInnlagte']
				dato_oppdatert = registrering['dato']
	
	for foretak in covid_data:
		for registrering in foretak['covidRegistreringer']:
			antall_innlagte_foretak = registrering['antInnlagte']
		totalt_innlagte = totalt_innlagte + int(antall_innlagte_foretak)
	return antall_innlagte_sshf, dato_oppdatert, str(totalt_innlagte)


def writeKratosData(filename, value):
    filepath = "/home/pi/kratosdata/" + filename
    file = open(filepath, "w")
    file.write(value)
    file.close()


def main(argv):
	global config

	yr_data = get_yr_data()
	print(yr_data)

    

if __name__ == "__main__":
	config = ConfigObj(os.path.expanduser('~') + '/.config/Helsedirektoratet/covid.conf')
	main(sys.argv[1:])