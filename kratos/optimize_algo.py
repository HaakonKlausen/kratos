import datetime
import time 

import kratoslib
import kratosdb

import constants
import devices 


class DummyDevice:
    def set_power(self, power):
        kratoslib.writeKratosLog('ERROR', f"Dummy Device Setting power to {power}")


class OptimizeDevice:

    def __init__(self, device, numberOfHours, numberOfMinutesEachHour, minimumTemperature=constants.EOL, maximumTemperature=constants.EOL * -1):
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
        if powerstate_str == "Av" or powerstate_str == "":
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


    def setPower(self, currentTemperature, devicename, frost_override=False, start_power=constants.Power.Off):
        power = start_power
        # Get desired powerstate based upon state and time
        if self.__state == constants.State.AllwaysOn:
            power = constants.Power.On
        elif self.__state == constants.State.AllwaysOff:
            power = constants.Power.Off
        if (self.__state == constants.State.Optimze) or ((self.__state == constants.State.AllwaysOff) and frost_override == True):
            power = self.__optimize()
            # Check if temperature limits should override
            if currentTemperature > self.__maximumTemperature:
                power = constants.Power.Off
                kratoslib.writeKratosLog('INFO', f"Temperature for device {devicename} above maximum")
            if currentTemperature < self.__minimumTemperature:
                power = constants.Power.On 
                kratoslib.writeKratosLog('INFO', f"Temperature for device {devicename} below minimum")
        kratoslib.writeKratosLog('INFO', f"Setting power for {devicename} to {power}")
        device.set_power(power)

    def setHeatpumpPower(self, currentTemperature, devicename, frost_override=False, start_power=constants.Power.Off):
        current_power = self.__device.get_current_powerstate()
        current_temperature = self.__device.get_temperature()
        power = current_power
        if current_power == constants.Power.Off:
            if current_temperature < self.__minimumTemperature:
                power = constants.Power.On 
                kratoslib.writeKratosLog('INFO', f"Temperature for device {devicename} below minimum while off, turning on")
                device.set_power(power)
        if current_power == constants.Power.On:
            if current_temperature > self.__maximumTemperature:
                power = constants.Power.Off
                kratoslib.writeKratosLog('INFO', f"Temperature for device {devicename} above maximum while on, turning off")
                device.set_power(power)

if __name__ == "__main__":
    kratosdata = kratosdb.kratosdb()

    frost_override = False
    out_temp = float(kratosdata.getMinimumTimeSeriesValue('hytten.out.temp', 56))
    if out_temp < 0.0:
        frost_override = True
        kratoslib.writeKratosLog('INFO', 'Frost override activated at Bjønntjønn')
        
    device =  devices.CottageHotwaterDevice()
    optimizer = OptimizeDevice(device=device, numberOfHours=6, numberOfMinutesEachHour=45, minimumTemperature=5.0)
    optimizer.setPower(currentTemperature=float(device.get_temperature()), devicename='Bjønntjønn Hotwater', frost_override=frost_override)

    device =  devices.CottageKitchenCabinet()
    optimizer = OptimizeDevice(device=device, numberOfHours=24, numberOfMinutesEachHour=45, minimumTemperature=5.0, maximumTemperature = 8.0)
    optimizer.setPower(currentTemperature=float(device.get_temperature()), devicename='Bjønntjønn Frostsikring Kjøkken', frost_override=frost_override)

    device =  devices.CottageWaterIntakeHeat()
    optimizer = OptimizeDevice(device=device, numberOfHours=24, numberOfMinutesEachHour=60)
    optimizer.setPower(currentTemperature=float(device.get_temperature()), devicename='Bjønntjønn Varmekabel Inntaksrør', frost_override=frost_override)

    device =  devices.CottageOvnerstueDevice()
    optimizer = OptimizeDevice(device=device, numberOfHours=8, numberOfMinutesEachHour=60, minimumTemperature=5.5, maximumTemperature=11.0)
    optimizer.setPower(currentTemperature=float(device.get_temperature()), devicename='Bjønntjønn Ovner Stue', frost_override=frost_override)

    device = devices.HomeHotwaterDevice()
    optimizer = OptimizeDevice(device=device, numberOfHours=6, numberOfMinutesEachHour=45)
    optimizer.setPower(currentTemperature=constants.EOL, devicename='Odderhei Hotwater')

    currentHour = datetime.datetime.now().hour
    currentMinute = datetime.datetime.now().minute
    weekday = datetime.datetime.now().weekday

    minimumTemperature=19.5
    maximumTemperature=20.5

    if currentHour >= 4 and currentHour <= 6:
        if not (currentHour == 5 and currentMinute >=45 and weekday <=4):
            maximumTemperature = maximumTemperature + 2
            minimumTemperature = minimumTemperature + 2

    if currentHour >=17:
            maximumTemperature = maximumTemperature + 0.5
            minimumTemperature = minimumTemperature + 0.5
        
    device = devices.HomeHeatpumpDevice()
    optimizer = OptimizeDevice(device=device, numberOfHours=8, numberOfMinutesEachHour=60, minimumTemperature=minimumTemperature, maximumTemperature=maximumTemperature)
    optimizer.setHeatpumpPower(currentTemperature=float(device.get_temperature()), devicename='Odderhei Varmepumpe')
    