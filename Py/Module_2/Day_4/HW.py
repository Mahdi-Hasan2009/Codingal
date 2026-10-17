number = int(input("Enter a number: "))
binary = ""

copy = number

for i in range(number):
    if copy == 0:
        break
    digit = copy % 2
    binary = str(digit) + binary
    copy = copy // 2

print("Binary:", binary)

