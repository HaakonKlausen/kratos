import teslapy
import kratoslib

class TeslaApi:
    def __init__(self):
        with teslapy.Tesla('hakon.klausen@icloud.com') as tesla:
            vehicles = tesla.product_list()
            #vehicles[0].sync_wake_up()
            vehicles[0].get_vehicle_data()
            #print(vehicles[0])
            self.__soc = float(vehicles[0]['charge_state']['battery_level'])
            self.__charge_power = float(vehicles[0]['charge_state']['charger_power'])
            self.__charge_state = (vehicles[0]['charge_state']['charging_state'])
            self.__charge_limit_soc = float(vehicles[0]['charge_state']['charge_limit_soc'])
            self.__charger_actual_current = float(vehicles[0]['charge_state']['charger_actual_current'])
            self.__minutes_to_full_charge = float(vehicles[0]['charge_state']['minutes_to_full_charge'])
            self.__driving = 'False'
            self.__drive_state = 'False'
            self.__speed = 0
            self.__odometer = 0
            if 'drive_state' in vehicles[0]:
                if vehicles[0]['drive_state']['shift_state'] == None:
                    self.__drive_state = 'False'
                else:
                    self.__drive_state = vehicles[0]['drive_state']['shift_state']
                    if self.__drive_state in ('D', 'R', 'N'):
                        self.__driving = 'True'
                if vehicles[0]['drive_state']['speed'] == None:
                    self.__speed = 0
                else:
                    self.__speed = round(float(vehicles[0]['drive_state']['speed']) * 1.60934)
            if 'vehicle_state' in vehicles[0]:
                if 'odometer' in vehicles[0]['vehicle_state']:
                    self.__odometer = round(float(vehicles[0]['vehicle_state']['odometer'])* 1.60934)

    def print_info(self):
        print(f"SOC: {self.__soc}")
        print(f"Charge power: {self.__charge_power}")
        print(f"Charge state: {self.__charge_state}")
        print(f"Charge limit SOC: {self.__charge_limit_soc}")
        print(f"Charger actual current: {self.__charger_actual_current}")
        print(f"Minutes to full charge: {self.__minutes_to_full_charge}")
        print(f"Drive state: {self.__drive_state}")
        print(f"Speed: {self.__speed}")
        print(f"Odometer: {self.__odometer}")
        #print(f"Charge cable: {self.__conn_charge_cable}")
        #print(f"Car version: {self.__car_version}")

    def store_test_info(self):
        print("Storing test data...")
        kratoslib.writeStatuslogData('tesla.online', 'True')
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
        kratoslib.writeTimeseriesData('tesla.speed', self.__speed)
        kratoslib.writeStatuslogData('tesla.drive_state', self.__drive_state)
        kratoslib.writeStatuslogData('tesla.driving', self.__driving)
        if self.__driving == 'False':
            if self.__odometer > 0:
                kratoslib.writeTimeseriesData('tesla.odometer', self.__odometer)
        else:
            odometer_start = int(round(float(kratoslib.readKratosData('tesla.odometer'))))
            kratoslib.writeTimeseriesData('tesla.currentDistance', self.__odometer - odometer_start)


if __name__ == "__main__":
    tesla_api = TeslaApi()
    tesla_api.store_info()
    tesla_api.print_info()