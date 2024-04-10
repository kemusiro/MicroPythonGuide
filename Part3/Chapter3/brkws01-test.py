import uasyncio
from machine import Pin, UART
from common.network import BRKWS01

async def main():
    # UARTのインスタンスを構築する。
    uart = UART(0, 9600, tx=Pin(16), rx=Pin(17), timeout=200, timeout_char=200)
    # SigFoxのインスタンスを構築する。
    sigfox = BRKWS01(uart)
    # SigFoxのタスクを開始する。
    sigfox.start()

    print(await sigfox.get_id())
    print(await sigfox.get_PAC())
    print(await sigfox.send_data("0123456789AB"))

uasyncio.run(main())
