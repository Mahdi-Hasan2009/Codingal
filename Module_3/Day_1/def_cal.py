def add(num1,num2):
  return num1+num2
def sub(num1,num2):
  return num1-num2
def mul(num1,num2):
  return num1*num2
def div(num1,num2):
  return num1/num2
def exp(num1,num2):
  return num1**num2
def flo(num1,num2):
  return num1//num2
def mod(num1,num2):
  return num1%num2



num1 = float(input("Enter Number 1: "))
num2 = float(input("Enter Number 2: "))
operator =input("Enter +, -, *, / , **,//,%: ")

if operator == "+":
  print(add(num1,num2)) 
elif operator == "-":
  print(sub(num1,num2))
elif operator == "*":
  print(mul(num1,num2))
elif operator == "/":
  print(div(num1,num2))
elif operator == "**":
  print(exp(num1,num2))
elif operator == "//":
  print(flo(num1,num2))
elif operator == "%":
  print(mod(num1,num2)) 
else:
  print("Invalid Operator")