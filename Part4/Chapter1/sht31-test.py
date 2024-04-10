import time
from machine import I2C
from machine import Pin
from common.device import SHT31

i2c = I2C(0)
sensor = SHT31(i2c)
while True:
    temperature, humidity = sensor.measure()
    print(f'temp = {temperature}, hum = {humidity}')
    time.sleep(1)
