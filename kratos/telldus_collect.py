import yaml 
import kratoslib
import telldus_api



class TelldusCollect:
    def __init__(self):
        __filepath = 'telldus_sensors.yaml'
        with open(__filepath, mode="rt", encoding="utf-8") as file:
            self.__sensors = yaml.safe_load(file)
        api = telldus_api.telldus_api()
        #db = kratosdb.kratosdb()
        for sensor in self.__sensors:
            print(f"Sensor: {sensor['name']}: {sensor['id']}")
            temp, humidity = api.getSensorInfo(sensor['id'], 'temp', 'humidity')
            print(temp, humidity)
            kratoslib.writeTimeseriesData(f"{sensor['name']}.temp", temp)
            kratoslib.writeTimeseriesData(f"{sensor['name']}.humidity", humidity)

if __name__ == "__main__":
    collector = TelldusCollect()