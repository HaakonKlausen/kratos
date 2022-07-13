import serial
import base64
import time
import binascii

import kratoslib

global data_raw

# https://www.skekraft.se/wp-content/uploads/2021/03/Aidon_Feature_Description_RJ12_HAN_Interface_EN.pdf


#        let meterId = buffer.slice(0, 16).toString();
#        let a_plus = parseInt(new Uint64LE(buffer.slice(16, 24)));     //Målerstand?
#        let a_minus = parseInt(new Uint64LE(buffer.slice(24, 32)));
#        let r_plus = parseInt(new Uint64LE(buffer.slice(32, 40)));
#        let r_minus = parseInt(new Uint64LE(buffer.slice(40, 48)));
#        let p_plus = buffer.readUInt16LE(48);                          //Active Power?
#        let p_minus = buffer.readUInt16LE(52);
#        let q_plus = buffer.readUInt16LE(56);
#        let q_minus = buffer.readUInt16LE(60);
#        let phi1 = buffer.readUInt16LE(64);
#        let phi2 = buffer.readUInt16LE(66);
#        let phi3 = buffer.readUInt16LE(68);
#        let p1 = buffer.readUInt32LE(70);
#        let p2 = buffer.readUInt32LE(74);
#        let p3 = buffer.readUInt32LE(78);
#        let u1 = buffer.readUInt16LE(82);
#        let u2 = buffer.readUInt16LE(84)
#        let u3 = buffer.readUInt16LE(86);;
#        let i1 = buffer.readUInt16LE(88);
#        let i2 = buffer.readUInt16LE(90);
#        let i3 = buffer.readUInt16LE(92);
#        let f = buffer.readUInt16LE(94);
#        let phases = buffer.readUInt8(96);


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

def readUIntLE(start_pos, length):
	value=0
	factor=1
	for i in range (0, length):
		value=value+(int(data_raw[start_pos + i]) * factor)
		factor = factor * 256
	return value

def find_prior_active_energy():
	sql = ("SELECT created, value FROM timeseries WHERE seriesname='bjonntjonn.oss.active_energy' ORDER BY created desc LIMIT 1")
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

def parse_message():
    active_power = str(readUIntLE(48, 2))
    active_energy = str(readUIntLE(16, 8))
    
    kratoslib.writeKratosData('bjonntjonn.oss.active_power', active_power)
    kratoslib.writeTimeseriesData('bjonntjonn.oss.active_power', active_power)

    kratoslib.writeKratosData('bjonntjonn.oss.active_energy', active_energy)
    # ToDo: Creating hourly active energy timeseries

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
				parse_message()
		time.sleep(1)

	except Exception as e:
		print('error in reading: ' + str(e))
		pass

  