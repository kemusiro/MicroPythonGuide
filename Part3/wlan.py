try:
    import network
    import time

    def init_wlan(ssid, password):
        # ステーション・モード接続用のオブジェクトを生成
        wlan = network.WLAN(network.STA_IF)
        # Wi-Fiインターフェースを有効化
        wlan.active(True)
        if not wlan.isconnected():
            # Wi-Fiアクセス・ポイントに接続する。
            wlan.connect(ssid, password)
            # IPアドレスを取得するまで待つ。
            while wlan.status() != network.STAT_GOT_IP:
                print('waiting...')
                # 1秒待つ。
                time.sleep(1)
        return wlan
except ImportError:
    # networkモジュールを持たないボードの場合は何もしない関数を定義する。
    def init_wlan(ssid, password):
        pass
