age = int(input("Enter your age: "))
isweekend = input("Is it weekend: ")
#13-60
if age >=13 and age<=60:
  if isweekend =="yes":
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