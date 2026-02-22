def squares(a, b):
    for i in range(a, b + 1):
        yield i * i


a = int(input("Enter start (a): "))
b = int(input("Enter end (b): "))

for value in squares(a, b):
    print(value)