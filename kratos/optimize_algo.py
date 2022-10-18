import datetime
import time 

import kratoslib
import kratosdb

import constants

class DummyDevice:
    def set_power(self, power):
        print(f"Setting power to {power}")


class OptimizeDevice:

    def __init__(self, device, state, numberOfHours, numberOfMinutesEachHour, minimumTemperature, maximumTemperature):
        self.__db = kratosdb.kratosdb()
        self.__device = device
        self.__state = state
        self.__numberOfHours = numberOfHours
        self.__numberOfMinutesEachHour = numberOfMinutesEachHour
        self.__minimumTemperature = minimumTemperature
        self.__maximumTemperature = maximumTemperature


    def finish(self):
        self.__db.close_connection()

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


    def setPower(self, currentTemperature):
        power = constants.Power.Off
        print(power)
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
        device.set_power(power)

if __name__ == "__main__":
    device = DummyDevice()
    optimizer = OptimizeDevice(device=device, state=constants.State.Optimze, numberOfHours=8, numberOfMinutesEachHour=60, minimumTemperature=5, maximumTemperature=22)
    optimizer.setPower(currentTemperature=20)