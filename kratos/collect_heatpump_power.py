import kratoslib 
import panasonic_api
import datetime
import time

class CollectHeatpumpPower:
    def __init__(self):
        self.__panasonic=panasonic_api.PanasonicApi()

    def dateToStr(self, date):
        datestr=date.strftime("%Y%m%d")
        return datestr

    def collect_date(self, date):
        datestr = self.dateToStr(date)
        history=self.__panasonic.get_hourly_power_consumption(datestr)
        for hour_consumption in history:
            hour=hour_consumption['hour']
            consumpition=hour_consumption['consumption']
            timestr = date.strftime("%Y-%m-%d ") + f'{hour:02}:00:00'
            storedate = datetime.datetime.strptime(timestr, "%Y-%m-%d %H:%M:%S")
            if consumpition >= 0.0:
                kratoslib.upsertTimeseriesDataTime("panasonic.active_energy", consumpition, storedate)
                print(storedate, consumpition)



if __name__ == "__main__":
    collector=CollectHeatpumpPower()
    history = collector.collect_date(datetime.datetime.today() + datetime.timedelta(days=0))
