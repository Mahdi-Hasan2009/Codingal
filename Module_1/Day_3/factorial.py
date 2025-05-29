x= int(input("Enter a Number: "))

factorial = 1


if x<0 :
  print("Please Give a Positive Number")
elif x==0 :
  print("1")
else:
  for i in range(1,x+1):
    factorial*= i 
  print(f"Factorial of {x} is {factorial} ")
  
  '''Problem:
Write a program that prints numbers from 1 to 50. But for multiples of 3, print "Fizz" instead of the number, and for multiples of 5, print "Buzz". For numbers which are multiples of both 3 and 5, print "FizzBuzz".'''
  
  
  