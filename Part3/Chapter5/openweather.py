import json
import urequests
from common.network import init_wlan
import secrets

# OpenWeatherで取得したAPIキー
API_KEY = "XXXXXXXX"
# 気象情報を取得したい都市名
CITY = "Tokyo"

wlan = init_wlan(secrets.WIFI_SSID, secrets.WIFI_PASSWORD)

resp = urequests.get(
    "https://api.openweathermap.org/data/2.5/weather"
    f"?q={CITY}&units=metric&APPID={API_KEY}")
d = json.loads(resp.text)

print("天気: {}".format(d["weather"][0]["main"]))
print("気温: {}".format(d["main"]["temp"]))
print("気圧: {}".format(d["main"]["pressure"]))
print("湿度: {}".format(d["main"]["humidity"]))
print("風速: {}".format(d["wind"]["speed"]))
