import uasyncio as asyncio
from common.network import UARTProxy

# ESP32のATコマンド・モードを使ってWi-Fiに接続するクラス
class ESP32AT(UARTProxy):
    def __init__(self, uart, *, qsize=10):
        # 親クラスのインスタンス生成関数を呼びだす。
        super().__init__(uart, qsize)

    # ATコマンドモードの改行コードを定義する。
    def newline(self):
        return b"\r\n"
    
    # ATコマンドモードのプロンプトを定義する。
    def prompt(self):
        return b""
    
    # ATコマンドの応答メッセージを解析する。
    async def parse(self):
        result = list()
        # エコーバックされるコマンドと改行を読み飛ばす。
        await self._queue.get()
        await self._queue.get()
        
        token = await self._queue.get()
        while token not in (b"OK", b"ERROR", b"SEND OK", b"SEND FAIL", b"SET OK"):
            # 応答コード以外のトークンの場合は文字コードをUTF-8に変換してからキューに積む。
            result.append(token.decode("utf-8"))
            token = await self._queue.get()
        result.append(token.decode("utf-8"))
        # 末尾のプロンプトを削除
        token = await self._queue.get()
        return result

    async def sender(self, line):
        # ATコマンド・モードは1行256バイトの制限があるのでエラーチェックをする。
        if len(line) >= 256:
            raise ValueError("Length of a message must be less than 256.")
        # 親クラスのsender関数を呼びだす。
        return await super().sender(line)

    # ATコマンドモードを使ってWi-Fiアクセス・ポイントに接続する。
    async def connect_wifi(self, ssid, password):
        print(await self.sender("AT+CWMODE=1"))
        print(await self.sender(f'AT+CWJAP="{ssid}","{password}"'))
        print(await self.sender("AT+CIPSTA?"))
    
    # MQTTのパラメータを設定する。
    async def mqtt_setconf(self, client_id, host, port):
        self._mqtt_client_id = client_id
        self._mqtt_host = host
        self._mqtt_port = port
        print(await self.sender('AT+MQTTCLEAN=0'))
        print(await self.sender(f'AT+MQTTUSERCFG=0,1,"{client_id}","","",0,0,""'))
        print(await self.sender(f'AT+MQTTCONN=0,"{host}",{port},0'))

    # MQTT publishを実行する。
    async def mqtt_publish(self, topic, message, qos):
        print(await self.sender(f'AT+MQTTPUB=0,"{topic}","{message}",{qos},0'))

