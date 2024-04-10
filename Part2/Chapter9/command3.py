class Item:
    def __init__(self, name):
        self.item_name = name

    def get_name(self):
        return self.item_name
    
obj1 = Item("apple")
obj2 = Item("orange")
print(obj1.get_name())
print(obj2.get_name())

