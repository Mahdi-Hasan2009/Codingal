num = int(input("Enter a number: "))
even_odd = input("evensum or oddsum ?: ").lower()
evensum = 0
oddsum = 0

if even_odd == "evensum":
  for i in range(0,num+1,2):
    print(i)
    evensum += i
  print("Evensum = ",evensum)
elif even_odd == "oddsum":
  for i in range(1,num+1,2):
    print(i)
    oddsum += i
  print("Oddsum = ",oddsum)
else:
  print("Invalid Input")
  
  

