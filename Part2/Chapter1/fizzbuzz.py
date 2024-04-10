# 3の倍数のときFizz、5の倍数のときBuzz、
# 両方の倍数のときFizzBuzz、
# それ以外のとき数字を表示する。
for i in range(1, 17):
    if i % 15 == 0: # 3の倍数かつ5の倍数→15の倍数
        print("FizzBuzz")
    elif i % 3 == 0:
        print("Fizz")
    elif i % 5 == 0:
        print("Buzz")
    else:
        print(i)

