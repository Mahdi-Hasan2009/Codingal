'''num1 = float(input("Enter your 1st Number: "))
num2 = float(input("Enter your 2nd Number: "))
num3 = float(input("Enter your 3rd Number: "))

print(f"{num3},{num1},{num2}")
'''
num = int(input("Enter number to swap: "))

temp = num %10 
swapped_num = str(temp)+str(num//10)

print(f"swap num: {swapped_num}")


