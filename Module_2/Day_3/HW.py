num = int(input("Enter a number: "))
sum = 0
temp = num
num_index = len(str(num))
while temp > 0:
  digit = temp % 10
  sum += digit ** num_index
  temp //= 10


if num == sum:
  print(num, "is an Armstrong number")
else:
  print(num, "is not an Armstrong number")