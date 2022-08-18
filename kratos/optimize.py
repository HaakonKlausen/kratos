import datetime
import time 

import kratoslib
import kratosdb
import telldus_api

#
# To be run periodically (every 5 minutes) to optimize a device based upon parameters:
#	Telldus Device ID
#	Number of lowest hours to use
#	Number of minutes to power on each hour
# 
# Based upon giving the device power from the start of the period.  Will turn off
# the device if the number of minutes is exceeded

class optimzeDevice:
	def __init__(self, deviceId, numberOfHours, numberOfMinutesEachHour):
		self.__db = kratosdb.kratosdb()
		self.__deviceId = deviceId
		self.__numberOfHours = numberOfHours
		self.__numberOfMinutesEachHour = numberOfMinutesEachHour


	def finish(self):
		self.__db.close_connection()


	def hourWithinNLowest(self, hour: int):
		# We schedule the minutes to be run at the end of the hour.
		# This way, it can be turned off towards the end of the hour to avoid 
		# using too much energy.
		# Check if minutes are to be started
		minutes = datetime.datetime.now().minute
		if minutes < 60 - self.__numberOfMinutesEachHour:
			kratoslib.writeKratosLog('DEBUG', 'Antall minutter per time ikke ennå påbegynt')
			return False

		# Get the hours of the lowest price
		sql = f"SELECT period FROM dayahead WHERE pricearea='NO2' AND pricedate = CURDATE() order by pricenoknet ASC LIMIT {self.__numberOfHours}"
		cursor = self.__db.get_cursor()
		cursor.execute(sql)
		within = False
		for period in cursor:
			if period[0] == hour:
				within = True
				break
		
		return within




def main():
	api = telldus_api.telldus_api()
	# Bjonntjonn optimizer
	# Check for away status
	bjonntjonn_hours = 4
	if kratoslib.readKratosData('bjonntjonn_preparing') == 'True':
		bjonntjonn_hours = 24
		kratoslib.writeKratosLog('INFO', 'Bjønntjønn will be preparing, hours set to 18')

	if kratoslib.readKratosData('bjonntjonn_away') == 'True':
		kratoslib.writeKratosLog('INFO', 'Bjønntjønn is in status Away, Water Heater remains off')
		kratoslib.writeStatuslogData('Bjønntjønn_Bereder', 'Off')
		kratoslib.writeTimeseriesData('bjonntjonn.bereder','0')
	else:
		optimizer = optimzeDevice('11020052', bjonntjonn_hours, 30)
		currentHour = datetime.datetime.now().hour

		if optimizer.hourWithinNLowest(currentHour):
			api.turnOn('11020052')
			kratoslib.writeKratosLog('INFO', 'Slår på VV bereder Bjønntjønn')
			kratoslib.writeStatuslogData('Bjønntjønn_Bereder', 'On')
			kratoslib.writeTimeseriesData('bjonntjonn.bereder','1')
		else:
			api.turnOff('11020052')
			kratoslib.writeKratosLog('INFO', 'Slår av VV bereder Bjønntjønn')
			kratoslib.writeStatuslogData('Bjønntjønn_Bereder', 'Off')
			kratoslib.writeTimeseriesData('bjonntjonn.bereder','0')
		optimizer.finish()

	#api = telldus_api.telldus_api()
	#api.turnOff('11020052')

	optimizer = optimzeDevice('1828820', 6, 45)
	currentHour = datetime.datetime.now().hour
	if optimizer.hourWithinNLowest(currentHour):
		api.turnOn ('1828820')
		kratoslib.writeKratosLog('INFO', 'Slår på VV bereder Odderhei')
		kratoslib.writeStatuslogData('Odderhei_Bereder', 'On')
		kratoslib.writeTimeseriesData('odderhei.bereder','1')
	else:
		api.turnOff ('1828820')
		kratoslib.writeKratosLog('INFO', 'Slår av VV bereder Odderhei')
		kratoslib.writeStatuslogData('Odderhei_Bereder', 'Off')
		kratoslib.writeTimeseriesData('odderhei.bereder','0')
	optimizer.finish()

	

if __name__ == "__main__":
	main()