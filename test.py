import random
from constants import *
import datetime

class WeatherWarning:
    def rain(self):
        print("Ожидаются сильные дожди и ливни с грозой")
    def snow(self):
        print("Ожидается снег и усиление ветра")
    def low_temperature(self):
        print("Ожидается сильное понижение температуры")

class WeatherWarningWithDate(WeatherWarning):
    def rain(self, date):
        print(date)
        super().rain()
    def snow(self, date):
        super().snow()
        print(date)
    def low_temperature(self, date):
        super().low_temperature()
        print(date)


from datetime import date

weatherwarning = WeatherWarningWithDate()
dt = date(2022, 12, 12)

weatherwarning.rain(dt)
weatherwarning.snow(dt)
weatherwarning.low_temperature(dt)

# print(tuple(a + b for a, b in zip(random.choice(list(DIRECTIONS.values())), (30, 34))))
