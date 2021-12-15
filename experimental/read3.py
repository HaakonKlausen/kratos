import serial
import base64
import time
import binascii

global data_raw

def parse_data(start_pos, length):
	data = ''
	for j in range (0, length):
		data = data + ' ' + str(int(data_raw[start_pos + j]))
	return data

def readUIntBE(start_pos, length):
	value=0
	factor=1
	print('length ', length)
	for i in range (0, length):
		print(i, int(data_raw[start_pos + length - 1 - i]))
		value=value+(int(data_raw[start_pos + length - 1 - i]) * factor)
		factor = factor * 256
	return value

def parse_message(start_pos):
	#print('Parsing from ' + str(start_pos))
	message=''
	for i in range (0, 6):
		message = message + '.' + str(data_raw[start_pos + i])
	subtype = str(data_raw[start_pos + 7])

	is_message=True

	if message == '.1.1.0.0.5.255':
		print(start_pos, 'MeterId', parse_data(start_pos+ 6, 8))
	elif message == '.1.1.96.1.1.255':
		print(start_pos, 'MeterType', parse_data(start_pos+ 6, 8))	
	elif message == '.1.1.1.7.0.255':
		print(start_pos, 'Active Power+', parse_data(start_pos+ 6, 8), readUIntBE(start_pos+7, 4))
	elif message == '.1.1.2.7.0.255':
		print(start_pos, 'Active Power-', parse_data(start_pos+ 6, 8))
	elif message == '.1.1.3.7.0.255':
		print(start_pos, 'Reactive Power+', parse_data(start_pos+ 6, 8))
	elif message == '.1.1.4.7.0.255':
		print(start_pos, 'Reactive Power-', parse_data(start_pos+ 6, 8))

	elif message == '.1.1.31.7.0.255':
		print(start_pos, 'IL1', parse_data(start_pos+ 6, 8))
	elif message == '.1.1.51.7.0.255':
		print(start_pos, 'IL2', parse_data(start_pos+ 6, 8))
	elif message == '.1.1.71.7.0.255':
		print(start_pos, 'IL3', parse_data(start_pos+ 6, 8))

	elif message == '.1.1.32.7.0.255':
		print(start_pos, 'VL1', parse_data(start_pos+ 6, 8))
	elif message == '.1.1.52.7.0.255':
		print(start_pos, 'VL2', parse_data(start_pos+ 6, 8))
	elif message == '.1.1.72.7.0.255':
		print(start_pos, 'VL3', parse_data(start_pos+ 6, 8))
	else:
		is_message=False

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
			print(' ')
		time.sleep(1)

	except Exception as e:
		print('error in reading: ' + str(e))
		pass

  