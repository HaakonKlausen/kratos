import teslapy
import kratoslib

class TeslaApi:
    def __init__(self):
        with teslapy.Tesla('hakon.klausen@icloud.com') as tesla:
            vehicles = tesla.vehicle_list()
            vehicles[0].get_vehicle_data()
            #print(vehicles[0])
            self.__soc = float(vehicles[0]['charge_state']['battery_level'])
            self.__charge_power = float(vehicles[0]['charge_state']['charger_power'])
            self.__charge_state = (vehicles[0]['charge_state']['charging_state'])
            self.__charge_limit_soc = float(vehicles[0]['charge_state']['charge_limit_soc'])
            self.__charger_actual_current = float(vehicles[0]['charge_state']['charger_actual_current'])
            self.__minutes_to_full_charge = float(vehicles[0]['charge_state']['minutes_to_full_charge'])
        

    def print_info(self):
        print(f"SOC: {self.__soc}")
        print(f"Charge power: {self.__charge_power}")
        print(f"Charge state: {self.__charge_state}")
        print(f"Charge limit SOC: {self.__charge_limit_soc}")
        print(f"Charger actual current: {self.__charger_actual_current}")
        print(f"Minutes to full charge: {self.__minutes_to_full_charge}")
        #print(f"Charge cable: {self.__conn_charge_cable}")
        #print(f"Car version: {self.__car_version}")

    def store_test_info(self):
        print("Storing test data...")
        kratoslib.writeStatuslogData('tesla.online', 'True')
        kratoslib.writeStatuslogData('tesla.driving', 'False')
        kratoslib.writeTimeseriesData('tesla.currentDistance', 0)

    def store_info(self):
        self.store_test_info()
        kratoslib.writeKratosLog('INFO', f"SOC: {self.__soc}")
        kratoslib.writeKratosLog('INFO', f"Charge power: {self.__charge_power}")
        kratoslib.writeKratosLog('INFO', f"Charge state: {self.__charge_state}")

        kratoslib.writeTimeseriesData('tesla.targetSoc', self.__charge_limit_soc)
        kratoslib.writeTimeseriesData('tesla.chargePower', self.__charge_power)
        kratoslib.writeTimeseriesData('tesla.remainingChargeTime', self.__minutes_to_full_charge)
        kratoslib.writeStatuslogData('tesla.plug', self.__charge_state)
        kratoslib.writeTimeseriesData('tesla.soc', self.__soc)


if __name__ == "__main__":
    tesla_api = TeslaApi()
    tesla_api.store_info()
    #tesla_api.print_info()