import kratoslib 
import panasonic_api
import datetime
import pytz

class CollectHeatpumpPower:
    def __init__(self):
        print("Init was here")
        self.__panasonic=panasonic_api.PanasonicApi()

    def dateToStr(self, date):
        datestr=date.strftime("%Y%m%d")
        return datestr

    def collect_date(self, date):
        datestr = self.dateToStr(date)
        print(f"Getting history for {datestr}")
        history=self.__panasonic.get_hourly_power_consumption(datestr)
        print(history)
        for hour_consumption in history:
            print(hour_consumption)
            hour=hour_consumption['hour']
            consumpition=hour_consumption['consumption']
            print(f"hour:{hour} {consumpition}")
            timestr = date.strftime("%Y-%m-%d ") + f'{hour:02}:00:00'
            storedate = datetime.datetime.strptime(timestr, "%Y-%m-%d %H:%M:%S")
            local_tz = pytz.timezone('CET')
            valid_time = True
            try:
                local_storedate = local_tz.localize(storedate, is_dst=None)
            except Exception as e:
                valid_time = False
            if valid_time:
                utc_storedate = local_storedate.astimezone(pytz.utc)
                if consumpition >= 0.0:
                    kratoslib.upsertTimeseriesDataTime("panasonic.active_energy", consumpition, utc_storedate)

    def collect_status(self):
        self.__panasonic.store_power_temperature()


if __name__ == "__main__":
    print("main was here")
    collector=CollectHeatpumpPower()
    history = collector.collect_date(datetime.datetime.today() + datetime.timedelta(days=0))
    collector.collect_status()
