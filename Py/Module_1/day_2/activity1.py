a = input("Enter Side A: ")
b = input("Enter Side B: ")
c = input("Enter Side C: ")

if a+b>c or b+c>a or a+c>b :
  print("This is a Triangle")
  if a == b == c:
    print("It is Equilateral Triangle")
  elif a == b or  b == c or c == a:
    print("It is Isosceles Triangle")
  else:
    print("It is Scalene Triangle")
else:
  print("Invalid Values of Triangle")
 


