num = int(input("Enter a number: "))

if num<2:
  print("It is not a prime number")
else:
  for i in range(2,num):
    if num % i==0:
      print("It is not a prime number")
      break
  else:
    print("It is a prime number")
      
      
    
    