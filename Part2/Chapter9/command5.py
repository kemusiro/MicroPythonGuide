# 武器の共通クラス
class Item:
    def __init__(self, price):
        self.price = price
        
    def do_attack(self):
        return "do nothing"
    
    def get_price(self):
        return self.price

# 剣
class Sword(Item):
    def do_attack(self):
        return "剣を振る"

# 棍棒
class Stick(Item):
    def do_attack(self):
        return "棍棒で叩く"
    
# パーティを組むメンバ
class Character:
    def __init__(self, name, item):
        self.my_name = name
        self.my_item = item
        
    def do_attack(self):
        my_name = self.my_name
        item_price = self.my_item.get_price()
        attack = self.my_item.do_attack()
        print(f"{my_name}は{item_price}円の{attack}")
 
# パーティのメンバを構成する。
party = [Character("アリス", Sword(1000)),
         Character("ボブ", Stick(200))]

# パーティのメンバが攻撃を行う。
for member in party:
    member.do_attack()

