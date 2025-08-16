num = [1,2,3,4,5,6]
sum = 0
for i in range(len(num)):
  print(num[i])
  sum+=num[i]
print(f"sum: {sum}")
print(f"average: {sum/len(num)}")