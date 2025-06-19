is_std = input("Are you student (yes/no): ").lower()

if is_std =="yes":
  age = int(input("Enter your age: "))
  if age >= 10 and age <= 20 :
    print("Successfully Enrolled")
  else:
    print("Devoid")
else:
  print("Devoid")
  