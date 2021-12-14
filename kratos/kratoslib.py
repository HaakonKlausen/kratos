import datetime
import os
from pathlib import Path 

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

def getKratosConfigFile(configfile):
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
        file.write(datetime.datetime.now().strftime("%a %-d %b %H:%M:%S %Y") + severity + ': ' + message)
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
    try:
        value = file.read()
    except Exception as e:
        writeKratosLog('ERROR', 'Unable to read ' + filename + ': ' + e.value)
    file.close()
    return value.strip()

def writeKratosData(filename, value):
    filepath=os.path.join(getKratosDisplayFolder(), filename)
    file = open(filepath, "w")
    file.write(value)
    file.close()


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
    writeKratosData('yr.period_start', '1979-01-01T00:00:00Z')
    writeKratosData('yr.precipitation_amount', '0')
    writeKratosData('yr.symbol_code', 'heavyrainandthunder')
    writeKratosData('yr.wind_from_direction', '0')
    writeKratosData('yr.wind_speed', '0')

#
# Check for the existence of folders and create if needed
#
def checkAndInitKratos():
    # Check for the existence of the display folder and create it if needed.
    # This will also make sure that the .config/kratos folder exists
    if Path(getKratosDisplayFolder()).exists() == False:
        print('INFO: Initializing Kratos...')
        try:
            os.makedirs(getKratosDisplayFolder())
        except Exception as e:
            print('ERROR: Unable to create the Kratos Display folder: ' + e.value)
    
        # Write default values
        initiateDisplayValues()
        # Create the Log file
        writeKratosLog('INFO', 'Kratos initialized', mode="w")
