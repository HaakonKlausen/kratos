import serial
import base64
import time
import binascii


def parse(encodedMBusPackage, bytesRead):
    print('Parsing package...')
    print(len(encodedMBusPackage))
    message = ''
    text = ''
    ncharinline = 0
    
    print(encodedMBusPackage[0])

    for i in range(len(encodedMBusPackage)):
        print('.1')
        message = message + char(encodedMBusPackage[i]).encode("hex") + ' '
        print('.2')
        text = text + encodedMBusPackage[i]
        print('.3')
        ncharinline = ncharinline + 1
        print('.4')
        if ncharinline > 20:
            ascii = binascii.b2a_qp(text, quotetabs=True, header=True)
            print(message + ' ' + ascii)
            ncharinline = 0
            message = ''
            text = ''
    ascii = binascii.b2a_qp(text, quotetabs=True, header=True)
    print(message + ' ' + ascii)


ser = serial.Serial('/dev/ttyUSB0', timeout=None, baudrate=115000, xonxoff=False, rtscts=False, dsrdtr=False)
ser.flushInput()
ser.flushOutput()
messages = 0
while messages < 30: 
    messages = messages + 1
    try:
        bytesToRead = ser.inWaiting()
        if bytesToRead > 0:
            print('bytes to read: ' + str(bytesToRead))
            data_raw = ser.read(bytesToRead)
            #print('Line read....' + (data_raw))
            ascii = binascii.b2a_qp(data_raw, quotetabs=True, header=True)
            #print (ascii)
            if bytesToRead > 2:
                parse(data_raw, bytesToRead)
            #data_bytes = data_raw.encode('ascii')
            #message_bytes = base64.b64decode(data_raw,)
            #print('line decoded...')
            #message = data_raw.decode('hex')
            #print(message)
        #else:
        #    print('Nothing to read')
        time.sleep(1)

    except Exception as e:
        print('error in reading: ' + str(e))
        pass

  