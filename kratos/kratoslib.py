import datetime
import os
import pytz
from configobj import ConfigObj
from pathlib import Path 
import mysql.connector

#
# Functions to get various locations
#
def getKratosHome():
    return str(Path(os.path.dirname(os.path.abspath(__file__))))

def getYrSymbolFolder():
    return os.path.join(getKratosHome(), 'yr-weather-symbols', 'png')

def getYrSymbolFilePath(filename):
    return os.path.join(getYrSymbolFolder(), filename)

def getImagesFolder():
    return os.path.join(getKratosHome(), 'images')

def getImageFilePath(filename):
    return os.path.join(getImagesFolder(), filename)

def getKratosConfigFolder():
    return os.path.join(str(Path.home()), '.config', 'kratos')

def getKratosDisplayFolder():
    return os.path.join(getKratosConfigFolder(), 'display')

def getKratosConfigFilePath(configfile):
    return os.path.join(getKratosConfigFolder(), configfile)

def getKratosLogFile():
    return os.path.join(getKratosConfigFolder(), 'kratos.log')

#
# Logging
#
def writeKratosLog(severity, message, mode="a"):
    try:
        file=open(getKratosLogFile(), mode)
    except FileNotFoundError:
        # Giving up, printing error to console
        print('ERROR: Unable to open Kratos log: ' + message)
    try:
        file.write(datetime.datetime.now().strftime("%a %d %b %H:%M:%S %Y") + ' App ' + severity + ': ' + message + '\n')
    except Exception as e:
        print('ERROR: Unable to write to Kratos log: ' + message + ': ' + e.value)
    file.close()

#
# Read and write display data
#
def readKratosData(filename):
	filepath=os.path.join(getKratosDisplayFolder(), filename)
	value = ''
	try:
		file = open(filepath, "r")
	except FileNotFoundError as e:
		writeKratosLog('ERROR', 'Kratos data ' + filename + ' does not exist. ')
		return value
	try:
		value = file.read()
	except Exception as e:
		writeKratosLog('ERROR', 'Unable to read ' + filename + ': ' + e.value)
		return value
	file.close()
	return value.strip()

def writeKratosData(filename, value):
	checkAndInitKratos()
	filepath=os.path.join(getKratosDisplayFolder(), filename)
	file = open(filepath, "w")
	file.write(str(value))
	file.close()
	writeKratosLog('DEBUG', 'Kratosdata written: ' + filename + ':' + str(value))
	writeKratosDataToSql(filename, value)


#
# Read and write config data
#
def readKratosConfigData(filename):
    filepath=os.path.join(getKratosConfigFolder(), filename)
    value = ''
    try:
        file = open(filepath, "r")
    except FileNotFoundError as e:
        writeKratosLog('ERROR', 'Kratos config ' + filename + ' does not exist. ')
    try:
        value = file.read()
    except Exception as e:
        writeKratosLog('ERROR', 'Unable to read ' + filename + ': ' + e.value)
    file.close()
    return value.strip()

def writeKratosConfigData(filename, value):
    filepath=os.path.join(getKratosConfigFolder(), filename)
    file = open(filepath, "w")
    file.write(value)
    file.close()
    writeKratosLog('DEBUG', 'Kratos Config written: ' + filename + ':' + value)


# 
# Get database connection
#
def getConnection():
	config = ConfigObj(getKratosConfigFilePath('kratosdb.conf'))

	try:
		connection = mysql.connector.connect(user=config['user'], password=config['password'],
								host=config['host'],
								database=config['database'])
		return connection

	except Exception as e:
		print('Error: ' + str(e))
		writeKratosLog('ERROR', 'Error in getting connection: ' + str(e))

	return

def writeKratosDataToSql(dataname, value):
	connection=getConnection()
	sql = ("select count(*) cnt from kratosdata where dataname=%(dataname)s")
	data = (dataname)
	count = 0
	cursor=connection.cursor()
	cursor.execute(sql, { 'dataname': dataname })
	for cnt in cursor:
		count = cnt[0]
	print(count)
	cursor.close()
	if count == 1:
		sql = ("UPDATE kratosdata set value=%s where dataname=%s")
		data=(value, dataname)
		cursor=connection.cursor()
		cursor.execute(sql, data)
	else:
		sql = ("INSERT INTO kratosdata(dataname, value) values (%s, %s)")
		data=(dataname, value)
		cursor=connection.cursor()
		cursor.execute(sql, data)

	connection.commit()
	cursor.close()
	connection.close()

def readKratosDataFromSql(dataname):
	connection=getConnection()
	sql = ("select value from kratosdata where dataname=%(dataname)s")
	retval = ''
	cursor=connection.cursor()
	cursor.execute(sql, { 'dataname': dataname })
	for val in cursor:
		retval = val[0]
	cursor.close()
	connection.close()
	return retval

def writeTimeseriesData(seriesname, value):
	sql = ("INSERT INTO timeseries (seriesname, created, value) "
			"VALUES (%s, %s, %s)")
	connection=getConnection()
	try:	
		cursor=connection.cursor()
		now=datetime.datetime.now(pytz.utc)
		data = (seriesname, now, value)
		cursor.execute(sql, data)
		connection.commit()
		cursor.close()
		connection.close()
	except Exception as e:
		writeKratosLog('ERROR', 'Error in storing timeseries ' + seriesname + ': ' + str(value) + ' (' + str(e) + ')')
	writeKratosLog('DEBUG', 'Kratos timeseries written: ' + seriesname + ':' + str(value))

#
# Initiate the display values
#
def initiateDisplayValues():
	writeKratosData('covid.date', 'Never')
	writeKratosData('covid.number', '0')
	writeKratosData('covid.sshf.number', '0')
	writeKratosData('in.humudity' ,'0')
	writeKratosData('in.temp' ,'0')
	writeKratosData('out.humudity' ,'0')
	writeKratosData('out.temp' ,'0')
	writeKratosData('marketstack.date' ,'Never')
	writeKratosData('marketstack.tsla', '1')
	writeKratosData('powerprice.eur', '0')
	writeKratosData('powerprice_max.eur', 0)
	writeKratosData('powerprice_3max.eur', 0)
	writeKratosData('powerprice_max.period', '0')
	writeKratosData('yr.period_start', '1979-01-01T00:00:00Z')
	writeKratosData('yr.precipitation_amount', '0')
	writeKratosData('yr.symbol_code', 'heavyrainandthunder')
	writeKratosData('yr.wind_from_direction', '0')
	writeKratosData('yr.wind_speed', '0')
	writeKratosData('oss.active_power', 0)

#
# Check for the existence of folders and create if needed
#
def checkAndInitKratos():
	# Check for the existence of the display folder and create it if needed.
	# This will also make sure that the .config/kratos folder exists
	if Path(getKratosDisplayFolder()).exists() == False:
		print('INFO: Initializing Kratos...')
		try:
			folderpath=getKratosDisplayFolder()
			print('Creating kratos config folder: ' + folderpath)
			os.makedirs(folderpath)
		except Exception as e:
			print('ERROR: Unable to create the Kratos Display folder: ')

		# Write default values
		initiateDisplayValues()
		# Create the Log file
		writeKratosLog('INFO', 'Kratos initialized', mode="w")
