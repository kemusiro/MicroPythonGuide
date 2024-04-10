import time
from machine import Pin
from common.device import HCSR04

sensor = HCSR04(Pin(config.HCSR04_TRIG, Pin.OUT),
                Pin(config.HCSR04_ECHO, Pin.IN))
while True:
    print(sensor.sense())
    time.sleep(0.1)
