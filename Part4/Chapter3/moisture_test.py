import time
from machine import ADC
from machine import Pin

if MYBOARD == "esp32":
    a = ADC(Pin(config.DEFAULT_ADC), atten=ADC.ATTN_11DB)
else:
    a = ADC(Pin(config.DEFAULT_ADC))

while True:
    print(a.read_u16())
    time.sleep(1)
    