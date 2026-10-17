num = int(input("Enter a number: "))
sum = 0
temp = num
count_num = len(str(num))
while temp > 0:
  digit = temp % 10
  sum += digit ** count_num
  temp //= 10


if num == sum:
  print(num, "is an Armstrong number")
else:
  print(num, "is not an Armstrong number")