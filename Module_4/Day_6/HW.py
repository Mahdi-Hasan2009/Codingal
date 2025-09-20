"""import random

def password_creator(passdigit=12):
  password = ""
  for i in range(passdigit):
      code = random.randint(33, 126)  
      password += chr(code)           
  return password

# Example
print("8 letter password:", password_creator(8))
print("12 letter password:", password_creator(12))
print("16 letter password:", password_creator(16))"""
x = input("Enter your password: ")

def valid(x):
  return any(i.islower() for i in x) and any(i.isupper() for i in x) and any(i.isdigit() for i in x) and any(33 <= ord(i) <= 64 for i in x)

if valid(x) == 0:
  print("The password is unsecure.")
else:
  print('The password is secure.")')