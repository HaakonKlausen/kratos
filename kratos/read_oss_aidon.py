import serial
import base64
import time
import binascii
import os
import kratoslib
import json

global data_raw

def parse_data(start_pos, length):
	data = ''
	for j in range (0, length):
		data = data + ' ' + str(int(data_raw[start_pos + j]))
	return data

def readUIntBE(start_pos, length):
	value=0
	factor=1
	for i in range (0, length):
		value=value+(int(data_raw[start_pos + length - 1 - i]) * factor)
		factor = factor * 256
	return value

def find_prior_active_energy():
	sql = ("SELECT created, value FROM timeseries WHERE seriesname='hytten_oss.active_energy' ORDER BY created desc LIMIT 1")
	connection=kratoslib.getConnection()
	cursor=connection.cursor()
	cursor.execute(sql)
	prior_value=0.0
	for (created, value) in cursor:
		prior_value = value
	kratoslib.writeKratosLog('DEBUG', 'Find prior active energy: prior value is ' + str(prior_value))
	try:
		cursor.close()
		connection.close()
	except:
		pass
	return prior_value

def writePowerToJSON(value:int):
	filepath=os.path.join('/var/www/html/kratosdata', 'hytten_active_power.json')
	file = open(filepath, "w")
	power_json = {
		"hytten_active_power": int(value),
		"id": "hytten.power01",
		"name": "Power Hytten",
		"connected": "true"
	}
	power_json_readable = json.dumps(power_json, indent=4)
	file.write(power_json_readable)
	#file.write("{" "oss.active_energy": {value}}')
	file.close()

def writeTotalEnergyToJSON(value:int):
	filepath=os.path.join('/var/www/html/kratosdata', 'hytten_total_energy.json')
	file = open(filepath, "w")
	power_json = {
		"hytten_total_energy": int(value),
		"id": "hytten.totalenergy01",
		"name": "Total Energy Hytten",
		"connected": "true"
	}
	power_json_readable = json.dumps(power_json, indent=4)
	file.write(power_json_readable)
	#file.write("{" "oss.active_energy": {value}}')
	file.close()

def writePeriodEnergyToJSON(value:int):
	filepath=os.path.join('/var/www/html/kratosdata', 'hytten_period_energy.json')
	file = open(filepath, "w")
	power_json = {
		"hytten_period_energy": int(value),
		"id": "hytten.periodenergy01",
		"name": "Period Energy Hytten",
		"connected": "true"
	}
	power_json_readable = json.dumps(power_json, indent=4)
	file.write(power_json_readable)
	#file.write("{" "oss.active_energy": {value}}')
	file.close()


def parse_message(start_pos):
	message=''
	for i in range (0, 6):
		message = message + '.' + str(data_raw[start_pos + i])
	subtype = str(data_raw[start_pos + 7])
	if message == '.1.0.1.7.0.255':
		kratoslib.writeTimeseriesData('hytten_oss.active_power', float(str(readUIntBE(start_pos+7, 4))))
		writePowerToJSON(str(readUIntBE(start_pos+7, 4)))
	if message == '.1.0.1.8.0.255':
		active_energy=float(str(readUIntBE(start_pos+7, 4))) / 100
		kratoslib.writeKratosLog('DEBUG', 'Active Energy: ' + str(active_energy))
		kratoslib.writeKratosData('hytten_oss.active_energy', str(active_energy))
		writeTotalEnergyToJSON(active_energy)

		# Find prior value before we write current
		prior_value = 0
		try:
			prior_value = find_prior_active_energy()
		except Exception as e:
			kratoslib.writeKratosLog('ERROR', 'Find prior active energy failed: ' + str(e))
			# If no prior, use this as a starting prior.
		period_value = (active_energy - prior_value) * 1000
		kratoslib.writeTimeseriesData('hytten_oss.active_energy', active_energy)

		if prior_value > 0:
			kratoslib.writeTimeseriesData('hytten_oss.period_active_energy', period_value)
			writePeriodEnergyToJSON(period_value)

ser = serial.Serial('/dev/ttyUSB0', timeout=None, baudrate=115000, xonxoff=False, rtscts=False, dsrdtr=False)
ser.flushInput()
ser.flushOutput()
messages = 0
while True: 
	messages = messages + 1
	try:
		bytesToRead = ser.inWaiting()
		if bytesToRead > 0:
			data_raw = ser.read(bytesToRead)
			if bytesToRead > 2:
				for i in range (0, bytesToRead - 9):
					parse_message(i)
		time.sleep(1)

	except Exception as e:
		kratoslib.writeKratosLog('ERROR', 'Read OSS Aidon: error in reading: ' + str(e))
		pass

  
