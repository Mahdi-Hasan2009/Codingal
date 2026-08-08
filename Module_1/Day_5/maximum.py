num1 = float(input("Enter Number 1: "))
num2 = float(input("Enter Number 2: "))
num3 = float(input("Enter Number 3: "))
'''
if num1<num2:
  if num2<num3:
    print(num3)
  else:
    print(num2)
else:
  if num1<num3:
    print(num3)
  else:
    print(num1)
'''

if num1>num2 and num1>num3:
  print(num1)
elif num2>num1 and num2>num3:
  print(num2)
else:
  print(num3)
