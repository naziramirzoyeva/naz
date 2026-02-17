import math 
a=int(input("Side length: "))
n=int(input( "Number of sides: "))
apofema=a/2*math.tan(math.pi/n)
area=(0.5*n*a*apofema)
final_a=math.ceil(area)
print("Area: ", final_a)