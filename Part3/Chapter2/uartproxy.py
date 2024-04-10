import uasyncio
from common.utils import Queue

class UARTProxy:
    def __init__(self, uart, qsize):
        self._uart = uart
        self._queue = Queue(qsize)
        # 非同期処理に対応したストリーム処理用オブジェクトを生成する。
        self._sreader = uasyncio.StreamReader(self._uart)
        self._swriter = uasyncio.StreamWriter(self._uart)
        
    # ボード固有の改行コード文字列を返す。
    def newline(self):
        raise NotImplementedError()
    
    # 外付けモジュールが返すプロンプト文字列を返す。
    def prompt(self):
        raise NotImplementedError()
    
    # 応答メッセージを解析する。
    def parse(self):
        raise NotImplementedError()

    # 受信タスクを開始する。
    def start(self):
        uasyncio.create_task(self.receiver())

    # 送信処理を行うコルーチン
    # 引数lineは文字列型のデータとする。
    async def sender(self, line):
        print("--- SEND: {}".format(line))
        # コマンドに改行コードを付加してStreamWriter内部のバッファに書き込む。
        self._swriter.write(line.encode() + self.newline())
        # バッファの内容をUARTに掃き出す。
        await self._swriter.drain()
        return await self.parse()

    # 受信処理を行うコルーチン
    async def receiver(self, rsize=64):
        # 受信データの末尾となる文字列を定義しておく。
        # プロンプトが存在しないボードでは末尾は空行(b"")となる。
        tail = b"" if self.prompt() is None else self.prompt()
        buffer = b""
        while True:
            # UARTから受信データが届くのを待つ。
            buffer += await self._sreader.read(rsize)
            strips = buffer.split(self.newline())
            # 受信データの末尾が改行またはプロンプト文字列でなければ後続のreadで行の残りを
            # 受信するはずなので、未処理の文字列としてバッファに移動しておく。
            buffer = strips.pop(-1) if strips[-1] != tail else b""
            for s in strips:
                await self._queue.put(s)