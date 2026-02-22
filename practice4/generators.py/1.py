def s(N):
    for i in range(1, N + 1):
        yield i * i



N = int(input())

for square in s(N):
    print(square)