from machine import Pin, time_pulse_us
import time

class HCSR04:
    def __init__(self, trigger, echo):
        self._trigger = trigger
        self._echo = echo
        self._trigger.value(0)
        
    def _speed_of_sound(self):
        return 340.0 # m/s
        
    def sense(self):
        # cm単位での距離を返す。
        self._trigger.value(1)
        time.sleep_us(10)
        self._trigger.value(0)

        duration = time_pulse_us(self._echo, 1, 30*1000)
        distance = (duration / 2) / 1_000_000 * self._speed_of_sound() * 100
        if distance < 2.0 or distance > 400.0:
            return -1
        else:
            return distance
