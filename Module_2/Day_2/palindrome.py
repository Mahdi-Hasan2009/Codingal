str1 = input("Enter a string: ")
str2 = ""

for i in str1:
  str2= i + str2
print("Reverse string: ",str2)

if str1 == str2 :
  print("It is a palindrome number")