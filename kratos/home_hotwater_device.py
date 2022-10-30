import telldus_api
import constants 

class HomeHotwaterDevice:
	def __init__(self):
		self.__telldus_api = telldus_api.telldus_api()

	def set_power(self, power):
		if power == constants.Power.On:
			self.__telldus_api.turnOn(constants.OdderheiHotwater)
		else:
			self.__telldus_api.turnOff(constants.OdderheiHotwater)
	
	def set_temperature(self, temperature):
		raise Exception ("Home Hotwater device does not support set_temperature")
	
	def get_temperature(self):
		return constants.EOL

	def get_powerstate_key(self):
		return "odderhei.bereder_setting"

if __name__ == "__main__":
	device = HomeHotwaterDevice()
	#device.set_power(constants.Power.Off)
	print(device.get_temperature())