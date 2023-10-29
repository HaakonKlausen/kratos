import datetime
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
            _, priorupdated = kratoslib.getLatestTimeSeriesData(f"{sensor['name']}.temp")
            new_value=False
            if priorupdated is None:
                new_value=True
            else:
                if lastUpdated > priorupdated:
                    new_value=True
            if new_value:
                kratoslib.writeKratosLog('DEBUG', f"New value for Sensor: {sensor['name']}: {sensor['id']}: {temp}/{humidity} updated {lastUpdated}, prior update: {priorupdated} ")
                kratoslib.writeTimeseriesData(f"{sensor['name']}.temp", temp, updated=lastUpdated)
                kratoslib.writeTimeseriesData(f"{sensor['name']}.humidity", humidity)
            else:
                timediff = datetime.datetime.now() - priorupdated
                minutes = int(round(timediff.total_seconds() / 60, 0))
                severity = 'WARN'
                if minutes > 30:
                    severity = 'ERROR'
                kratoslib.writeKratosLog(severity, f"No new value for Sensor: {sensor['name']}: {sensor['id']}, prior update at {priorupdated}, {minutes} minutes ago ")

if __name__ == "__main__":
    collector = TelldusCollect()