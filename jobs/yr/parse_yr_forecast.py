#!/usr/bin/python3

import sys
import getopt
import os
import json
import requests
from requests_oauthlib import OAuth1 as oauth
from configobj import ConfigObj
import http.client, urllib.request, urllib.parse, urllib.error, base64
from prodict import Prodict

def get_yr_data():
    yr_file = open('/home/pi/kratosdata/yr_forecast.json')
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
        period_start = prop['time']
        break
    print(wind_speed, symbol_code, precipitation_amount, period_start, wind_from_direction)
    return wind_speed, symbol_code, precipitation_amount, period_start, wind_from_direction

def writeKratosData(filename, value):
    filepath = "/home/pi/kratosdata/display/" + filename
    file = open(filepath, "w")
    file.write(value)
    file.close()

def main():
    wind_speed, symbol_code, precipitation_amount, period_start, wind_from_direction = get_yr_forecast()
    writeKratosData('yr.wind_speed', str(wind_speed))
    writeKratosData('yr.symbol_code', symbol_code)
    writeKratosData('yr.precipitation_amount', str(precipitation_amount))
    writeKratosData('yr.wind_from_direction', str(wind_from_direction))
    writeKratosData('yr.period_start', str(period_start))
    

main()