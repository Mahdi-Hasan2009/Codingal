rows = int(input("Enter Row: "))

for i in range(rows):
  for j in range(i+1):
    print("*",end=" ") 
  print()