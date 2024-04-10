import uasyncio
from common.network import UARTProxy

class BRKWS01(UARTProxy):
    def __init__(self, uart, *, qsize=10):
        super().__init__(uart, qsize)

    def newline(self):
        return b"\r\n"

    def prompt(self):
        return None

    async def parse(self):
        result = list()
        while ((token := await self._queue.get()) != b""):
            result.append(token.decode("utf-8"))
        return result

    # モジュールのIDを取得する。
    async def get_id(self):
        return await self.sender("AT$I=10")
    
    # モジュールのPACを取得する。
    async def get_PAC(self):
        return await self.sender("AT$I=11")

    # Sigfoxクラウドにデータを送信する。
    async def send_data(self, data):
        await self.sender(f"AT$SF={data}")