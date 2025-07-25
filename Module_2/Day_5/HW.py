rows = int(input("Enter Row: "))

for i in range(rows,-1,-1):
  for j in range(i+1):
    print("*",end=" ") 
  print()
