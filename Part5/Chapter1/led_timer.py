from machine import Pin
from machine import Timer
import time

state = 0
def toggle_led(t):
    global state
    led.value(state)
    state = 1 if state == 0 else 0
    
led = Pin(config.DEFAULT_LED, Pin.OUT)

t = Timer(config.DEFAULT_TIMER_ID)
t.init(period=100, callback=toggle_led)
time.sleep(3)
Timer.deinit(t)
# タイマーが非初期化するまで待つ。
time.sleep(0.1)
led.off()

