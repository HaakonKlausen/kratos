import panasonic_api
import constants

class HomeHeatpumpDevice:
	def __init__(self):
		self.__panasonic_api = panasonic_api.PanasonicApi()

	def set_power(self, power):
		if power == constants.Power.On:
			self.__panasonic_api.poweron()
		else:
			self.__panasonic_api.poweroff()
	
	def set_temperature(self, temperature):
		self.__panasonic_api.set_temperature(temperature)

	