import random
counter = 0
for _ in range(10000):
    v = random.randint(1, 10)
    if v != 1:
        continue
    counter += 1
print(counter)
