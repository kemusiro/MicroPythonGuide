class Parent():
    def __init__(self):
        print("parent")

class Child(Parent):
    def __init__(self):
        super().__init__()
        print("child")

c = Child()

