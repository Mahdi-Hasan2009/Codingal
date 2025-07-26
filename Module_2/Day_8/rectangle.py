import math

side1 = float(input("Enter side 1: "))
side2 = float(input("Enter side 2: "))



def perimeter(side1=0,side2=0):
  return 2 * (side1 + side2)
def area(side1=1,side2=1):
  return side1 * side2
def diagonal(side1=0,side2=0):
  return math.sqrt(side1**2 + side2**2)


print("perimeter :",perimeter(side1,side2))
print("area :",area(side1,side2))
print("diagonal :",diagonal(side1,side2))


