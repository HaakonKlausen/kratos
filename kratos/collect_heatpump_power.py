import kratoslib 
import panasonic_api
import datetime
import pytz

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
            local_tz = pytz.timezone('CET')
            local_storedate = local_tz.localize(storedate, is_dst=None)
            utc_storedate = local_storedate.astimezone(pytz.utc)
            if consumpition >= 0.0:
                kratoslib.upsertTimeseriesDataTime("panasonic.active_energy", consumpition, utc_storedate)



if __name__ == "__main__":
    collector=CollectHeatpumpPower()
    history = collector.collect_date(datetime.datetime.today() + datetime.timedelta(days=0))
