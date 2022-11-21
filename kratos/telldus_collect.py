import os
import yaml 
import kratoslib
import telldus_api



class TelldusCollect:
    def __init__(self):
        __filepath = os.path.join(kratoslib.getKratosHome(), 'telldus_sensors.yaml')
        with open(__filepath, mode="rt", encoding="utf-8") as file:
            self.__sensors = yaml.safe_load(file)
        api = telldus_api.telldus_api()
        #db = kratosdb.kratosdb()
        for sensor in self.__sensors:
            temp, humidity, lastUpdated = api.getSensorInfoUpdated(sensor['id'], 'temp', 'humidity')
            priorvalue, priorupdated = kratoslib.getLatestTimeSeriesData(f"{sensor['name']}.temp")
            if lastUpdated > priorupdated:
                kratoslib.writeKratosLog('DEBUG', f"New value for Sensor: {sensor['name']}: {sensor['id']}: {temp}/{humidity} updated {lastUpdated}, prior update: {priorupdated} ")
                kratoslib.writeTimeseriesData(f"{sensor['name']}.temp", temp, updated=lastUpdated)
                kratoslib.writeTimeseriesData(f"{sensor['name']}.humidity", humidity)
            else:
                kratoslib.writeKratosLog('WARN', f"No new value for Sensor: {sensor['name']}: {sensor['id']}, prior update: {priorupdated} ")

if __name__ == "__main__":
    collector = TelldusCollect()