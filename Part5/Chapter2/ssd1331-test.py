import math
import time
from machine import Pin, SPI
from common.device import SSD1331, fbcolor

spi = SPI(config.SSD1331_SPI_ID, baudrate=5_000_000,
          polarity=1, phase=1,
          sck=Pin(config.SSD1331_SPI_SCLK),
          mosi=Pin(config.SSD1331_SPI_MOSI),
          miso=Pin(config.SSD1331_SPI_MISO))

display = SSD1331(spi, 96, 64,
                  Pin(config.SSD1331_SPI_RESET, Pin.OUT),
                  Pin(config.SSD1331_SPI_DC, Pin.OUT),
                  Pin(config.SSD1331_SPI_CS, Pin.OUT))
display.reset()

# 描画する関数
def f(t):
    return 20 * math.sin(t) + 10 * math.sin(3 * t) + 32

t = 0
prev = 0
while True:
    y = int(f(t))
    # 1個前の点と現在の点を結ぶ直線を描画する。
    display.line(93, prev, 94, y, fbcolor(0.3, 0.8, 2))
    # 左方向に1ピクセル分シフトする。
    display.scroll(-1, 0)
    prev = y
    t += 0.3
    # フレームバッファの内容をディスプレイに送信する。
    display.update()
    time.sleep_ms(10)
    break