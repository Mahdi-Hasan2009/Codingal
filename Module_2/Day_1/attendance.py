attendance = int(input("Enter your attendance: "))
med = input("Enter your medical report: ")
if med =="yes":
  print("show prove")
else:
  if attendance >= 75 :
    print("you are selected")
  else:
    print("you are unselected")
