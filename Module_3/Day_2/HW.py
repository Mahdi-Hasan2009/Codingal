try:
  age = input("Enter your age: ")
  if not age.isdigit():
    raise ValueError("Invalid Input. Please Enter Integer Input")
  
  age_int = int(age)
  
  if age_int %2 == 0:
    print(f"{age}: Even")
  else:
    print(f"{age}: Odd")
    
except ValueError as ex:
  print("Error: ",ex)
finally:
  print("programme finished")
     