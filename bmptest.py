

import Adafruit_BMP.BMP085 as BMP085
from time import sleep
sensor = BMP085.BMP085()

while True:
    temperature = sensor.read_temperature()
    pressure = sensor.read_pressure()
    altitude = sensor.read_altitude()
    print temperature
    print pressure
    print altitude
    sleep(1)

