n = 4
for i in range(n):
    for j in range(n):
        if i >= j:
            continue
        print(i, j)
