import telldus_api
import panasonic_api

import constants 
import kratoslib 

class CottageHotwaterDevice:
	def __init__(self):
		self.__telldus_api = telldus_api.telldus_api()

	def set_power(self, power):
		if power == constants.Power.On:
			self.__telldus_api.turnOn(constants.BjonntjonnHotwater)
			kratoslib.writeStatuslogData('Bjonntjonn_Bereder', 'On')
			kratoslib.writeTimeseriesData('bjonntjonn.bereder','1')
		else:
			self.__telldus_api.turnOff(constants.BjonntjonnHotwater)
			kratoslib.writeStatuslogData('Bjonntjonn_Bereder', 'Off')
			kratoslib.writeTimeseriesData('bjonntjonn.bereder','0')

	def set_temperature(self, temperature):
		kratoslib.writeKratosLog('ERROR', 'Cottage Hotwater Device: Set Temperature not supported')

	def get_temperature(self):
		temp, _ = kratoslib.getLatestTimeSeriesData('hytten.bad.temp')
		return temp

	def get_powerstate_key(self):
		return "bjonntjonn.bereder_setting"


class CottageKitchenCabinet:
	def __init__(self):
		self.__telldus_api = telldus_api.telldus_api()

	def set_power(self, power):
		if power == constants.Power.On:
			self.__telldus_api.turnOn(constants.BjonntjonnKjokkenskapOvn)
			kratoslib.writeStatuslogData('Bjonntjonn_Kjokkenskap', 'On')
			kratoslib.writeTimeseriesData('bjonntjonn.kjokkenskap','1')
		else:
			self.__telldus_api.turnOff(constants.BjonntjonnKjokkenskapOvn)
			kratoslib.writeStatuslogData('Bjonntjonn_Kjokkenskap', 'Off')
			kratoslib.writeTimeseriesData('bjonntjonn.kjokkenskap','0')

	def set_temperature(self, temperature):
		kratoslib.writeKratosLog('ERROR', 'Cottage Kitchen Cabinet: Set Temperature not supported')

	def get_temperature(self):
		temp, _ = kratoslib.getLatestTimeSeriesData('hytten.kjokkenskap.temp')
		return temp

	def get_powerstate_key(self):
		return "bjonntjonn.kjokkenskap_setting"


class CottageWaterIntakeHeat:
	def __init__(self):
		self.__telldus_api = telldus_api.telldus_api()

	def set_power(self, power):
		if power == constants.Power.On:
			self.__telldus_api.turnOn(constants.BjonntjonnVarmekabelVann)
		else:
			self.__telldus_api.turnOff(constants.BjonntjonnVarmekabelVann)
	
	def set_temperature(self, temperature):
		kratoslib.writeKratosLog('ERROR', 'Cottage Water Intake: Set Temperature not supported')

	def get_temperature(self):
		temp, _ = kratoslib.getLatestTimeSeriesData('hytten.out.temp')
		return temp

	def get_powerstate_key(self):
		return "bjonntjonn.varmekabel_setting"


class CottageOvnerstueDevice:
	def __init__(self):
		self.__telldus_api = telldus_api.telldus_api()

	def set_power(self, power):
		if power == constants.Power.On:
			self.__telldus_api.turnOn(constants.BjonntjonnOvnBad)
			#self.__telldus_api.turnOn(constants.BjonntjonnOvnKjokken)
			self.__telldus_api.turnOn(constants.BjonntjonnOvnPeis)
			kratoslib.writeStatuslogData('Bjonntjonn_Ovner', 'On')
			kratoslib.writeTimeseriesData('bjonntjonn.ovner','1')
		else:
			self.__telldus_api.turnOff(constants.BjonntjonnOvnBad)
			#self.__telldus_api.turnOff(constants.BjonntjonnOvnKjokken)
			self.__telldus_api.turnOff(constants.BjonntjonnOvnPeis)
			kratoslib.writeStatuslogData('Bjonntjonn_Ovner', 'Off')
			kratoslib.writeTimeseriesData('bjonntjonn.ovner','0')

	def set_temperature(self, temperature):
		kratoslib.writeKratosLog('ERROR', 'Cottage Ovner Stue: Set Temperature not supported')

	def get_temperature(self):
		temp, _ = kratoslib.getLatestTimeSeriesData('hytten.in.temp')
		return temp

	def get_powerstate_key(self):
		return "bjonntjonn.ovnerstue_setting"


class HomeHotwaterDevice:
	def __init__(self):
		self.__telldus_api = telldus_api.telldus_api()

	def set_power(self, power):
		if power == constants.Power.On:
			self.__telldus_api.turnOn(constants.OdderheiHotwater)
			kratoslib.writeStatuslogData('Odderhei_Bereder', 'On')
			kratoslib.writeTimeseriesData('odderhei.bereder','1')
		else:
			self.__telldus_api.turnOff(constants.OdderheiHotwater)
			kratoslib.writeStatuslogData('Odderhei_Bereder', 'Off')
			kratoslib.writeTimeseriesData('odderhei.bereder','0')

	def set_temperature(self, temperature):
		kratoslib.writeKratosLog('ERROR', 'Home Hotwater Device: Set Temperature not supported')

	def get_temperature(self):
		return constants.EOL

	def get_powerstate_key(self):
		return "odderhei.bereder_setting"


class HomeHeatpumpDevice:
	def __init__(self):
		self.__panasonic_api = panasonic_api.PanasonicApi()

	def set_power(self, power):
		if power == constants.Power.On:
			self.__panasonic_api.set_temperature(23)
			kratoslib.writeStatuslogData('Odderhei_Varmepumpe', 'On')
			kratoslib.writeTimeseriesData('odderhei.varmepumpe','1')
		else:
			self.__panasonic_api.set_temperatureLowFan(19)
			kratoslib.writeStatuslogData('Odderhei_Varmepumpe', 'Off')
			kratoslib.writeTimeseriesData('odderhei.varmepumpe','0')

	def set_temperature(self, temperature):
		self.__panasonic_api.set_temperature(temperature)

	def get_temperature(self):
		temp, _ = kratoslib.getLatestTimeSeriesData('in.temp')
		return temp

	def get_powerstate_key(self):
		return "odderhei.varmepumpe_setting"

	def get_current_powerstate(self):
		current_state, _ = kratoslib.getLatestStatuslog('Odderhei_Varmepumpe')
		if str(current_state) == 'Off':
			return constants.Power.Off
		else:
			return constants.Power.On



if __name__ == "__main__":
	#device = CottageHotwaterDevice()
	#device.set_power(constants.Power.Off)
	device = HomeHeatpumpDevice()
	device.set_power(constants.Power.On)
	print(device.get_current_powerstate())