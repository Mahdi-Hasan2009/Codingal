'''word = input("Enter the word in lowercase: ")
upper = word.upper()
print("The word in uppercase is:",upper)'''

 
for i in range(1,51):
    if i % 3 == 0 and i % 5 == 0:
       print("FizzBuzz")
    elif i % 3 == 0:
       print("Fizz")
    elif i % 5 == 0:
       print("Buzz")
    else:
       print(i)