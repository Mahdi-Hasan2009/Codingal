num1 = float(input("Enter Number 1: "))
num2 = float(input("Enter Number 2: "))
operator =input("Enter +, -, *, / , **,//,%: ")

if operator == "+":
  print(num1+num2) 
elif operator == "-":
  print(num1-num2)
elif operator == "*":
  print(num1*num2)
elif operator == "/":
  print(num1/num2)
elif operator == "**":
  print(num1**num2)
elif operator == "//":
  print(num1//num2)
elif operator == "%":
  print(num1%num2) 
else:
  print("Invalid Operator")

  

