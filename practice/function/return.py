#1
def myfunc():
  x = 300
  print(x)

myfunc()

#2
def myfunc():
  x = 300
  def myinnerfunc():
    print(x)
  myinnerfunc()

myfunc()

#3
x = 300

def myfunc():
  print(x)

myfunc()

print(x)


#4
x = 300

def myfunc():
  x = 200
  print(x)

myfunc()

print(x)




#5
x = "global"

def outer():
  x = "enclosing"
  def inner():
    x = "local"
    print("Inner:", x)
  inner()
  print("Outer:", x)

outer()
print("Global:", x)




