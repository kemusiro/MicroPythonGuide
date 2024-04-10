import time
from machine import Pin, SPI
import framebuf

# RGBの各要素(0〜1.0)からピクセルのビット・パターンを作成する。
def fbcolor(r, g, b):
    r = int(r * 0x1f) & 0x1f
    g = int(g * 0x3f) & 0x3f
    b = int(b * 0x1f) & 0x1f
    v = ((g & 0x07) << 13) + (r << 8) + (b << 3) + ((g & 0x38) >> 3)
    return v

COLOR_BLACK = fbcolor(0, 0, 0)
COLOR_WHITE = fbcolor(1, 1, 1)

class SSD1331:
    _reset_sequence = (
        b"\xae",        # display off
        b"\xa0\x76",    # remap
        b"\xa1\x00",    # start line = 0
        b"\xa2\x00",    # vertical offset = 0
        b"\xa4",        # normal display
        b"\xa8\x3f",    # multplex ratio = 64
        b"\xad\x8e",    # set master configuration
        b"\x87\x0f",    # master current = 0x0f
        b"\x81\x80",    # contrast A = 0x80
        b"\x82\x80",    # contrast B = 0x80
        b"\x83\x80",    # contrast C = 0x80
        b"\xaf"         # display on
    )
    
    def __init__(self, spi, width, height, reset, dc, cs):
        self._spi = spi
        self._width = width
        self._height = height
        self._reset = reset
        self._dc = dc
        self._cs = cs
        self._buffer = bytearray(width * height * 2)
        self._fbuf = framebuf.FrameBuffer(self._buffer, width, height,
                                          framebuf.RGB565)
    
    # SPIデバイスにコマンドを送信する。
    def _send_command(self, command):
        try:
            self._cs.value(0)
            self._dc.value(0)
            self._spi.write(command)
        finally:
            self._cs.value(1)
            
    # SPIデバイスにｄデータを送信する。
    def _send_data(self, data):
        try:
            self._cs.value(0)
            self._dc.value(1)
            self._spi.write(data)
        finally:
            self._cs.value(1)

    # ディスプレイをリセットする。
    def reset(self):
        self._reset.value(1)

        self._cs.value(0)
        self._reset.value(0)
        time.sleep_us(3)
        self._reset.value(1)
        self._cs.value(1)
        
        for command in SSD1331._reset_sequence:
            self._send_command(command)

    # ディスプレイを背景色cでクリアする。
    def clear(self, c):
        self._fbuf.fill(c)

    # 指定した位置に文字列を表示する。
    def text(self, s, x, y, c=COLOR_WHITE):
        self._fbuf.text(s, x, y, c)

    # 指定した位置にピクセルを描画する。
    def pixel(self, x, y, c):
        self._fbuf.pixel(x, y, c)
        
    # 指定した2点間で直線を描画する。
    def line(self, x1, y1, x2, y2, c):
        self._fbuf.line(x1, y1, x2, y2, c)
        
    # ディスプレイを指定方向にシフトする。
    def scroll(self, xstep, ystep):
        self._fbuf.scroll(xstep, ystep)

    # フレームバッファの内容をディスプレイに一括送信する。
    def update(self):
        self._send_data(self._buffer)