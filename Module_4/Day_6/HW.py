import random

def password_creator(passdigit=12):
  password = ""
  for i in range(passdigit):
      code = random.randint(33, 126)  
      password += chr(code)           
  return password

# Example
print("8 letter password:", password_creator(8))
print("12 letter password:", password_creator(12))
print("16 letter password:", password_creator(16))
