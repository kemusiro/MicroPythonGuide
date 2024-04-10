from machine import Pin
import random
import time
from umqtt.simple import MQTTClient
from common.network import init_wlan
import secrets

# shiftr.ioで作成したインスタンスに従って設定する。
DOMAIN = "DOMAIN"
INSTANCE = "INSTANCE"
TOKEN = "TOKEN"

BROKER = DOMAIN + ".cloud.shiftr.io"

# 購読しているメッセージを受信したときに呼びだされるコールバック関数
def callback(topic, msg):
    print(f"received topic: {topic} message: {msg}")
    if topic == b"board/led":
        led = Pin(config.ONBOARD_LED, Pin.OUT)
        if msg == b"on":
            led.on()
        elif msg == b"off":
            led.off()
            
# Wi-Fiへの接続
wlan = init_wlan(secrets.WIFI_SSID, secrets.WIFI_PASSWORD)
print(wlan.ifconfig())

# MQTTクライアントの接続
mqtt = MQTTClient("picow", BROKER, port=1883,
                  user=INSTANCE, password=TOKEN)
mqtt.set_callback(callback)
mqtt.connect()

# トピックの購読
mqtt.subscribe(b"board/led")

# ブローカーからの送信されてきたメッセージの有無をチェックする。
while True:
    # メッセージを発行
    mqtt.publish(b"sensor/temperature",
                 str(random.randrange(0,100)).encode())
    mqtt.check_msg()
    time.sleep(1)
    
