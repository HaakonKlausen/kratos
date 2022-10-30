import telldus_api
import constants 

class CottageHotwaterDevice:
	def __init__(self):
		self.__telldus_api = telldus_api.telldus_api()

	def set_power(self, power):
		if power == constants.Power.On:
			self.__telldus_api.turnOn(constants.BjonntjonnHotwater)
		else:
			self.__telldus_api.turnOff(constants.BjonntjonnHotwater)
	
	def set_temperature(self, temperature):
		print("Not supported")


	def get_temperature(self):
		return constants.EOL

	def get_powerstate_key(self):
		return "bjonntjonn.bereder_setting"



if __name__ == "__main__":
	device = CottageHotwaterDevice()
	device.set_power(constants.Power.Off)