height = float(input("Enter Your Height: "))
weight = float(input("Enter Your Weight: "))
bmi = weight/(height**2)
print(f"Your BMI is: {bmi}")

if bmi<=24.9 and bmi>=18.5:
  print("you are normal weight")
elif bmi<=29.9 and bmi>=25.0:
  print("you are normal weight")
elif bmi<=34.9 and bmi>=30.0:
  print("you are obese class 1")
elif bmi<=39.9 and bmi>=35.0:
  print("you are obese class 2")
elif  bmi<=49.9 and bmi>=40.0:
  print("you are obese class 3")
elif bmi<=18.5:
  print("You are underweight")
else:
  print("Invalid BMI")
  
