try:
  num1,num2 = eval(input("Enter 2 numbers , separated by a comma : "))
  result = num1/num2
  print("Result is: ",result)
except ZeroDivisionError:
  print("Division by zero is error!")
except SyntaxError as ex :
  print(ex)
except:
  print("Wrong input")
else:
  print("No error")
finally:
  print("Finally part always can executed")
  