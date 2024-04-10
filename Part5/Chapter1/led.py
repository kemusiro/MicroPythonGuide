from machine import Pin
import time

led = Pin(config.DEFAULT_LED, Pin.OUT)
for _ in range(10):
    led.on()
    time.sleep_ms(200)
    led.off()
    time.sleep_ms(200)
