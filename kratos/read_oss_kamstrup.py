import serial
import base64
import time
import binascii
import os
import kratoslib
import json

global data_raw
global hourely_sum
global hourely_count

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
	sql = ("SELECT created, value FROM timeseries WHERE seriesname='oss.active_energy' ORDER BY created desc LIMIT 1")
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
	filepath=os.path.join('/var/www/html/kratosdata', 'huset_active_power.json')
	file = open(filepath, "w")
	power_json = {
		"huset_active_power": int(value),
		"id": "huset.power01",
		"name": "Power Huset",
		"connected": "true"
	}
	power_json_readable = json.dumps(power_json, indent=4)
	file.write(power_json_readable)
	#file.write("{" "oss.active_energy": {value}}')
	file.close()
	kratoslib.pushWWWFileToBjonntjonn("huset_active_power.json")

def writeTotalEnergyToJSON(value:int):
	filepath=os.path.join('/var/www/html/kratosdata', 'huset_total_energy.json')
	file = open(filepath, "w")
	power_json = {
		"huset_total_energy": int(value),
		"id": "huset.totalenergy01",
		"name": "Total Energy Huset",
		"connected": "true"
	}
	power_json_readable = json.dumps(power_json, indent=4)
	file.write(power_json_readable)
	#file.write("{" "oss.active_energy": {value}}')
	file.close()
	kratoslib.pushWWWFileToBjonntjonn("huset_total_energy.json")

def writePeriodEnergyToJSON(value:int):
	filepath=os.path.join('/var/www/html/kratosdata', 'huset_period_energy.json')
	file = open(filepath, "w")
	power_json = {
		"huset_period_energy": int(value),
		"id": "huset.periodenergy01",
		"name": "Period Energy Huset",
		"connected": "true"
	}
	power_json_readable = json.dumps(power_json, indent=4)
	file.write(power_json_readable)
	#file.write("{" "oss.active_energy": {value}}')
	file.close()
	kratoslib.pushWWWFileToBjonntjonn("huset_period_energy.json")

def parse_message(start_pos):
	global hourely_sum
	global hourely_count
	message=''
	for i in range (0, 6):
		message = message + '.' + str(data_raw[start_pos + i])
	subtype = str(data_raw[start_pos + 7])
	if message == '.1.1.1.7.0.255':
		power_str = str(readUIntBE(start_pos+7, 4))
		power = float(power_str)
		kratoslib.writeKratosData('oss.active_power', power_str)
		print(str(readUIntBE(start_pos+7, 4)))
		kratoslib.writeTimeseriesData('oss.active_power', power)
		writePowerToJSON(power_str)
		# Calculate hourely sum	
		hourely_sum = hourely_sum + power
		hourely_count = hourely_count + 1
		hourely_mean = hourely_sum / hourely_count
		kratoslib.writeEntityToJSON(hourely_mean, 'huset_mean_hourely_power', 'Huset Snitt Time Effekt')

	if message == '.1.1.1.8.0.255':
		active_energy=float(str(readUIntBE(start_pos+7, 4))) / 100
		kratoslib.writeKratosData('oss.active_energy', str(active_energy))
		writeTotalEnergyToJSON(active_energy)
		hourely_count = 0
		hourely_sum = 0
		# Find prior value before we write current
		prior_value = 0
		try:
			prior_value = find_prior_active_energy()
		except Exception as e:
			kratoslib.writeKratosLog('ERROR', 'Find prior active energy failed: ' + str(e))

		period_value = (active_energy - prior_value) * 1000
		kratoslib.writeTimeseriesData('oss.active_energy', active_energy)

		if prior_value > 0:
			kratoslib.writeKratosData('oss.period_active_energy', str(period_value))
			kratoslib.writeTimeseriesData('oss.period_active_energy', period_value)
			writePeriodEnergyToJSON(period_value)

writePowerToJSON("0")
ser = serial.Serial('/dev/ttyUSB0', timeout=None, baudrate=115000, xonxoff=False, rtscts=False, dsrdtr=False)
ser.flushInput()
ser.flushOutput()
messages = 0
hourely_count = 0
hourely_sum = 0
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
		print('error in reading: ' + str(e))
		pass

  
