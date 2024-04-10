import uasyncio
from machine import Pin, UART
from common.network import ESP32AT
import secrets
    
async def main():
    # UARTクラスのインスタンスを構築する。
    uart = UART(0, 115200, tx=Pin(16), rx=Pin(17), timeout=200, timeout_char=200)
    # ESP32ATクラスのインスタンスを構築する。
    esp32 = ESP32AT(uart)
    # ESP32を使った受信タスクを開始する。
    esp32.start()
    # ESP32を使ってWi-Fiへの接続とMQTTメッセージの発行を行う。
    await esp32.connect_wifi(secrets.WIFI_SSID, secrets.WIFI_PASSWORD)
    await esp32.mqtt_setconf("ESP32", "test.mosquitto.org", 1883)
    await esp32.mqtt_publish("/esp32at/data", "test", 0)

# メイン・タスクを開始する。
uasyncio.run(main())
