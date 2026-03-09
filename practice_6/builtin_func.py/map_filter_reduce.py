from functools import reduce

numbers = [1, 2, 3, 4, 5]

# map
squares = list(map(lambda x: x**2, numbers))
print("Squares:", squares)

# filter
even = list(filter(lambda x: x % 2 == 0, numbers))
print("Even numbers:", even)

# reduce
sum_numbers = reduce(lambda x, y: x + y, numbers)
print("Sum:", sum_numbers)