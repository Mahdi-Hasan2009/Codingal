age = int(input("Enter your age: "))

if age >=13 and age<=60:
  is_weekend = input("Is it weekend: ")
  if is_weekend =="yes":
    if age<=25 and age>=13:
      print("550tk")
    else:
      print("650tk")
  else:
    if age<=25 and age>=13:
      print("500tk")
    else:
      print("600tk")
else:
  print("You are not allowed")