import ujson
import urequests
import time
from machine import ADC
from machine import I2C
from machine import Pin
from machine import SPI
from common.network import init_wlan
from common.device import SSD1331, fbcolor
from common.device import SHT31
import secrets

API_URL = "https://script.google.com/macros/s/AKfycbyKFnS53stzXTGE9yXT9QkY3WR2PEq3Jte26U9blojRK6OT3QolySqvdzysaqdeusu5/exec"
WATERING_THRESHOLD = 30000

# Wi-Fiに接続
init_wlan(secrets.WIFI_SSID, secrets.WIFI_PASSWORD)

# 温湿度センサーを初期化
moist = ADC(Pin(26))
env = SHT31(I2C(1, sda=Pin(14), scl=Pin(15)))

# ディスプレイを初期化
spi = SPI(0, baudrate=5_000_000,
          polarity=1, phase=1,
          sck=Pin(18),
          mosi=Pin(19),
          miso=Pin(16))
display = SSD1331(spi, 96, 64,
                  Pin(20, Pin.OUT),
                  Pin(21, Pin.OUT),
                  Pin(17, Pin.OUT))
display.reset()

# 水やりモーター用GPIOの初期化
motor = Pin(22, Pin.OUT)

while True:
    try:
        # センサー・データを取得
        temperature, humidity = env.measure()
        moisture = moist.read_u16()
        
        # 情報を表示
        print(f"temp = {temperature}, humid = {humidity}, moist = {moisture}")
        display.clear(fbcolor(0, 0, 0))
        display.text(f"T: {temperature:.1f}", 0, 0, fbcolor(1, 0, 0))
        display.text(f"H: {humidity:.1f}", 0, 10, fbcolor(0, 0, 1))
        display.text(f"M: {moisture}", 0, 20, fbcolor(0, 1, 0))
        display.update()
        
        # 情報をクラウドに送信
        data = {"id": "picow", "temperature": temperature,
                "humidity": humidity, "moisture": moisture}
        resp = urequests.post(API_URL,
                              json=data)
        resp.close()
        resp = None

        # 水やりが必要な状態ならモーターを5秒間オンにする。
        if moisture > WATERING_THRESHOLD:
            motor.on()
            time.sleep(5)
            motor.off()
            
        # 10分間待つ
        time.sleep(10*60)
    except Exception:
        # すべての例外を捕捉しプログラムの実行を継続する。
        pass
    
