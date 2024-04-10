import struct
import time
from machine import I2C

DEFAULT_I2C_ADDRESS = 0x44

REP_HIGH = "High"
REP_MED = "Medium"
REP_LOW = "Low"

_COMMAND_TABLE = {
    REP_HIGH: 0x2400, REP_MED: 0x240b, REP_LOW: 0x2416
}

class SHT31:
    def __init__(self, i2c, *, repeatability=REP_HIGH, addr=DEFAULT_I2C_ADDRESS):
        self.i2c = i2c
        self.addr = addr
        self.repeatability = repeatability
        self._buffer = bytearray(6)
    
    # センサーのコマンドを送信する。
    def _send_command(self, command):
        self.i2c.writeto(self.addr, struct.pack(">H", command))
        
    # バイト列からCRC8を計算する。
    def _crc8(self, data):
        crc = 0xff
        for v in data:
            crc ^= v
            for _ in range(8):
                if crc & 0x80 != 0:
                    crc = (crc << 1) ^ 0x31
                else:
                    crc <<= 1
        return crc & 0xff
    
    # センサーから温度と湿度を取得する。
    def measure(self):
        command = _COMMAND_TABLE[self.repeatability]
        self._send_command(command)
        # デバイスの計測中の待ち時間
        time.sleep_ms(15)
        self.i2c.readfrom_into(self.addr, self._buffer)
        raw_t, crc_t, raw_h, crc_h = struct.unpack('>HBHB', self._buffer)
        if (self._crc8(self._buffer[0:2]) != crc_t or
            self._crc8(self._buffer[3:5]) != crc_h):
            print('不正なデータを受信しました。')
            return 0, 0
        else:
            temperature = -45 + 175 * (raw_t / 65535)
            humidity = 100 * (raw_h / 65535)
            return temperature, humidity