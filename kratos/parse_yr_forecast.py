#!/usr/bin/python3

import base64
import getopt
import json
import os
import requests
import sys

from configobj import ConfigObj
import http.client, urllib.request, urllib.parse, urllib.error
from prodict import Prodict
from requests_oauthlib import OAuth1 as oauth

import kratoslib


def get_yr_data():
    yr_file = open(kratoslib.getKratosConfigFilePath('yr_forecast.json'))
    return json.load(yr_file)

def get_yr_forecast():
	wind_speed = ''
	symbol_code = ''
	precipitation_amount = ''
	yr_data = get_yr_data()
	for prop in yr_data['properties']['timeseries']:
		#print(prop['time'])
		#print(prop['data']['instant']['details']['wind_speed'])
		#print(prop['data']['next_6_hours']['summary']['symbol_code'])
		wind_speed = prop['data']['instant']['details']['wind_speed']
		wind_from_direction = prop['data']['instant']['details']['wind_from_direction']
		symbol_code = prop['data']['next_6_hours']['summary']['symbol_code']
		precipitation_amount = prop['data']['next_6_hours']['details']['precipitation_amount']
		air_temperature = prop['data']['instant']['details']['air_temperature']
		period_start = prop['time']
		break
	return wind_speed, symbol_code, precipitation_amount, period_start, wind_from_direction, air_temperature


def main():
	kratoslib.writeKratosLog('DEBUG', 'Parsing Yr data')
	wind_speed, symbol_code, precipitation_amount, period_start, wind_from_direction, air_temperature = get_yr_forecast()
	kratoslib.writeKratosData('yr.wind_speed', str(wind_speed))
	kratoslib.writeKratosData('yr.symbol_code', symbol_code)
	kratoslib.writeKratosData('yr.precipitation_amount', str(precipitation_amount))
	kratoslib.writeKratosData('yr.wind_from_direction', str(wind_from_direction))
	kratoslib.writeKratosData('yr.period_start', str(period_start))
	kratoslib.writeKratosData('yr.air_temperature', str(air_temperature))
    
	kratoslib.writeTimeseriesData('yr.wind_speed', wind_speed)
	kratoslib.writeTimeseriesData('yr.precipitation_amount', precipitation_amount)
	kratoslib.writeTimeseriesData('yr.wind_from_direction', wind_from_direction)
	kratoslib.writeTimeseriesData('yr.air_temperature', air_temperature)
main()