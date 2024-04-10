import uasyncio

class Queue:
    # キューのインスタンスを生成する。
    def __init__(self, size=10):
        self._queue = list()
        self._size = size
        self._event_get = uasyncio.Event()
        self._event_put = uasyncio.Event()

    # キューが満杯かどうかを検査する。
    def is_full(self):
        return len(self._queue) == self._size
    
    # キューが空かどうかを検査する。
    def is_empty(self):
        return len(self._queue) == 0
    
    # キューの長さを返す。
    def size(self):
        return len(self._queue)
    
    # キューに要素を登録する。
    async def put(self, element):
        # キューが満杯の間待つ。
        while self.is_full():
            # キューから要素が取り出されたことを示すイベントを受信するのを待つ。
            await self._event_get.wait()
            self._event_get.clear()
        # キューに要素を追加したことを示すイベントを通知する。
        self._event_put.set()
        self._queue.append(element)
        
    # キューから要素を取り出す。
    async def get(self):
        # キューが空の間待つ。
        while self.is_empty():
            # キューに要素が追加されたことを示すイベントを受信するのを待つ。
            await self._event_put.wait()
            self._event_put.clear()
        # キューから要素が取り出されたことを示すイベントを通知する。
        self._event_get.set()
        return self._queue.pop(0)