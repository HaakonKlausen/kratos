import serial
import base64
import time
import binascii

import kratoslib

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

def parse_message(start_pos):
	#print('Parsing from ' + str(start_pos))
	message=''
	for i in range (0, 6):
		message = message + '.' + str(data_raw[start_pos + i])
	subtype = str(data_raw[start_pos + 7])
	if message == '.1.1.1.7.0.255':
		# print('Active Power+', readUIntBE(start_pos+7, 4))
		kratoslib.writeKratosData('oss.active_power', str(readUIntBE(start_pos+7, 4)))
		kratoslib.writeTimeseriesData('oss.active_power', float(str(readUIntBE(start_pos+7, 4))))
	if message == '.1.1.1.8.0.255':
		# print('Active Power+', readUIntBE(start_pos+7, 4))
		kratoslib.writeKratosData('oss.active_energy', str(readUIntBE(start_pos+7, 4)))
		kratoslib.writeTimeseriesData('oss.active_energy', float(str(readUIntBE(start_pos+7, 4))) / 100)
		# https://www.kode24.no/guider/smart-meter-part-1-getting-the-meter-data/71287300

ser = serial.Serial('/dev/ttyUSB0', timeout=None, baudrate=115000, xonxoff=False, rtscts=False, dsrdtr=False)
ser.flushInput()
ser.flushOutput()
messages = 0
while True: 
	messages = messages + 1
	try:
		bytesToRead = ser.inWaiting()
		if bytesToRead > 0:
			# print('bytes to read: ' + str(bytesToRead))
			data_raw = ser.read(bytesToRead)
			if bytesToRead > 2:
				for i in range (0, bytesToRead - 9):
					#print(str(int(data_raw[i])))
					parse_message(i)
		time.sleep(1)

	except Exception as e:
		print('error in reading: ' + str(e))
		pass

  