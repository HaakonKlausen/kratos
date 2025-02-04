import datetime
import os
import time
import yaml 
import kratoslib
import telldus_api_v2
import json



class TelldusCollect:
    def writeSensorToJSON(self, name: str, id: str, value:float):
        filepath=os.path.join("/var/www/html/kratosdata", f"{name}_temp.json")
        file = open(filepath, "w")
        power_json = {
            f"{name}_temp": float(value),
            "id": f"huset.{id}",
            "name": f"Temp {name}",
            "connected": "true"
        }
        power_json_readable = json.dumps(power_json, indent=4)
        file.write(power_json_readable)
        file.close()
        kratoslib.pushWWWFileToBjonntjonn(f"{name}_temp.json")


    def __init__(self):
        __filepath = os.path.join(kratoslib.getKratosHome(), 'telldus_sensors.yaml')
        with open(__filepath, mode="rt", encoding="utf-8") as file:
            self.__sensors = yaml.safe_load(file)
        api = telldus_api_v2.TelldusApi()
        #db = kratosdb.kratosdb()
        for sensor in self.__sensors:
            print("Waiting before loop...")
            time.sleep(240)
            temp, humidity, lastUpdated = api.getSensorInfoUpdated(sensor['id'], 'temp', 'humidity')
            print(f"Sensor {sensor['name']}/{sensor['id']}: Temperature {temp}, Humidity {humidity}")
            if temp is None:
                kratoslib.writeKratosLog('ERROR', f"Error getting sensor info for sensor: {sensor['name']}: {sensor['id']}")
                kratoslib.writeTimeseriesData(f"{sensor['name']}.temp", 99)
            else:
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
                    self.writeSensorToJSON(name=sensor['name'], id=sensor['id'], value=float(temp))
                else:
                    timediff = datetime.datetime.now() - priorupdated
                    minutes = int(round(timediff.total_seconds() / 60, 0))
                    severity = 'WARN'
                    if minutes > 30:
                        severity = 'ERROR'
                    kratoslib.writeKratosLog(severity, f"No new value for Sensor: {sensor['name']}: {sensor['id']}, prior update at {priorupdated}, {minutes} minutes ago ")

if __name__ == "__main__":
    collector = TelldusCollect()