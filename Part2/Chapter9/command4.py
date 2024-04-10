class Item:
    COMPANY_NAME = ""
    
    def __init__(self, name):
        self.item_name = name
        
    def change_company_name(self, name):
        Item.COMPANY_NAME = name

    def get_name(self):
        return f"{self.COMPANY_NAME}: {self.item_name}"
    
obj1 = Item("apple")
obj2 = Item("orange")
obj1.change_company_name("MyCompany")
print(obj1.get_name())
print(obj2.get_name())
