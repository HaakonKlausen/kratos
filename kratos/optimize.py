import datetime

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
		# Get the hours of the lowest price
		sql = f"SELECT period FROM dayahead WHERE pricearea='NO2' AND pricedate = CURDATE() order by price ASC LIMIT {self.__numberOfHours}"
		cursor = self.__db.get_cursor()
		cursor.execute(sql)
		within = False
		for period in cursor:
			print(str(period[0]))
			if period[0] == hour:
				within = True
				break
		
		return within




def main():
	# Bjonntjonn optimizer
	optimizer = optimzeDevice('11020052', 6, 30)
	currentHour = datetime.datetime.now().hour

	if optimizer.hourWithinNLowest(currentHour):
		print("Low price!")
	else:
		print("Turn it off!")
	
	optimizer.finish()
	api = telldus_api.telldus_api()
	api.turnOff('11020052')

if __name__ == "__main__":
	main()