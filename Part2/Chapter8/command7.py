# 価格リスト
price_list = {"apple": 100, "orange": 50, "bag": 3}

# 合計金額を求める。
def order(napple, norange, *, bag=False):
    price = napple * price_list["apple"] + norange * price_list["orange"]
    if bag:
        price += price_list["bag"]
    return price
