import datetime
import time 

import kratoslib
import kratosdb

import constants
import home_heatpump_device 
import home_hotwater_device
import cottage_hotwater_device


class DummyDevice:
    def set_power(self, power):
        print(f"Setting power to {power}")


class OptimizeDevice:

    def __init__(self, device, numberOfHours, numberOfMinutesEachHour, minimumTemperature=constants.EOL, maximumTemperature=constants.EOL):
        self.__db = kratosdb.kratosdb()
        self.__device = device
        self.__numberOfHours = numberOfHours
        self.__numberOfMinutesEachHour = numberOfMinutesEachHour
        self.__minimumTemperature = minimumTemperature
        self.__maximumTemperature = maximumTemperature
        self.__state = self.__get_powerstate(self.__device)


    def finish(self):
        self.__db.close_connection()


    def __get_powerstate(self, device):
        powerstate_str = self.__db.readKratosDataFromSql(device.get_powerstate_key())
        if powerstate_str == "Av":
            return constants.State.AllwaysOff
        elif powerstate_str == "Alltid På":
            return constants.State.AllwaysOn
        else:
            return constants.State.Optimze


    def __hourWithinNLowest(self, hour: int):
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

    def __optimize(self):
        currentHour = datetime.datetime.now().hour
        if self.__hourWithinNLowest(hour=currentHour):
            return constants.Power.On
        else:
            return constants.Power.Off


    def setPower(self, currentTemperature, devicename):
        power = constants.Power.Off
        # Get desired powerstate based upon state and time
        if self.__state == constants.State.AllwaysOn:
            power = constants.Power.On
        elif self.__state == constants.State.AllwaysOff:
            power = constants.Power.Off
        elif self.__state == constants.State.Optimze:
            power = self.__optimize()
            # Check if temperature limits should override
            if currentTemperature > self.__maximumTemperature:
                power = constants.Power.Off
            if currentTemperature < self.__minimumTemperature:
                power = constants.Power.On 
        print(power)
        kratoslib.writeKratosLog('INFO', f"Setting power for {devicename} to {power}")
        device.set_power(power)

if __name__ == "__main__":
    kratosdata = kratosdb.kratosdb()

    device = home_hotwater_device.HomeHotwaterDevice()
    optimizer = OptimizeDevice(device=device, numberOfHours=6, numberOfMinutesEachHour=45)
    optimizer.setPower(constants.EOL, 'Odderhei Hotwater')

    device = cottage_hotwater_device.CottageHotwaterDevice()
    optimizer = OptimizeDevice(device=device, numberOfHours=6, numberOfMinutesEachHour=45)
    optimizer.setPower(constants.EOL, 'Bjønntjønn Hotwater')

    #device = home_heatpump_device.HomeHeatpumpDevice()
    #optimizer = OptimizeDevice(device=device, numberOfHours=8, numberOfMinutesEachHour=60, minimumTemperature=17.0, maximumTemperature=20.0)
    #optimizer.setPower(currentTemperature=float(device.get_temperature()))
