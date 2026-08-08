import math
num = input('Enter a number: ')

if not num.isdigit():
    print("Invalid input. Please enter a number.")
else:
    num = float(num)  
    radians = math.radians(num)  
    print("Sin:", math.sin(radians))
    print("Cos:", math.cos(radians))
    print("Tan:", math.tan(radians))