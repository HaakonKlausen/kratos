import panasonic_api
import telldus_api

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


	def get_temperature(self):
		api = telldus_api.telldus_api()
		temp, _ = api.getSensorInfo(constants.OdderheiKitchenInTemp, 'temp', 'humidity')
		return temp

	def get_powerstate_key(self):
		return "odderhei.varmepumpe_setting"


if __name__ == "__main__":
	device = HomeHeatpumpDevice()
	#device.set_power(constants.Power.Off)
	print(device.get_temperature())