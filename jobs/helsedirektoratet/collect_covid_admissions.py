#!/usr/bin/python3
# -*- coding: utf-8 -*-

import sys
import getopt
import os
import json
import requests
from requests_oauthlib import OAuth1 as oauth
from configobj import ConfigObj
import http.client, urllib.request, urllib.parse, urllib.error, base64


def get_covid_data():
	global config 

	headers = {
		# Request headers
		'Ocp-Apim-Subscription-Key': config['subscriptionKey'],
	}


	params = urllib.parse.urlencode({
	})

	try:
		conn = http.client.HTTPSConnection('api.helsedirektoratet.no')
		conn.request("GET", "/ProduktCovid19/Covid19statistikk/helseforetak?%s" % params, "{body}", headers)
		response = conn.getresponse()
		data = response.read()
		#print(data)
		conn.close()
	except Exception as e:
		print("[Errno {0}] {1}".format(e.errno, e.strerror))

	return json.loads(data.decode('utf-8'))


def parse_covid_data(covid_data):
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
    filepath = "/home/pi/.config/kratos/display/" + filename
    file = open(filepath, "w")
    file.write(value)
    file.close()


def main(argv):
	global config
	if ('subscriptionKey' not in config or config['subscriptionKey'] == ''):
		print('ERROR: No Subscription Key in Config')
		return
	covid_data = get_covid_data()
	antall_innlagte_sshf, dato_oppdatert, totalt_innlagte = parse_covid_data(covid_data)

	dato = dato_oppdatert[8:10] + '.' + dato_oppdatert[5:7] + '.' + dato_oppdatert[2:4]
	print(dato, antall_innlagte_sshf, totalt_innlagte)
	writeKratosData('covid.sshf.number', str(antall_innlagte_sshf))
	writeKratosData('covid.number', str(totalt_innlagte))
	writeKratosData('covid.date', dato)
    

if __name__ == "__main__":
	config = ConfigObj(os.path.expanduser('~') + '/.config/Helsedirektoratet/covid.conf')
	main(sys.argv[1:])