year = int(input("Enter A Year: "))
if year % 400 ==0:
  print("It is a leapyear")
else:
  if year %4 == 0 and year % 100 != 0:
    print("It is a leapyear")
  else:
    print("It is not a leapyear")    
  