for i in range(1, 41):
    if i % 15 == 0:
     print("FizzBuzz") # 空白5文字
    elif i % 3 == 0:
        print("Fizz") # 空白8文字
    elif i % 5 == 0:
            print("Buzz") # 空白12文字
    else:
                print(i) # 空白16文字

