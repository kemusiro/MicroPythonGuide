from common.network import init_wlan
import secrets

wlan = init_wlan(secrets.WIFI_SSID, secrets.WIFI_PASSWORD)
status = wlan.ifconfig()
print(f'IP address {status[0]}')
print(f'Netmask {status[1]}')
print(f'Gateway {status[2]}')
print(f'DNS Server {status[3]}')

