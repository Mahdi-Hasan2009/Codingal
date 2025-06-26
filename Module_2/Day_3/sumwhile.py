num = int(input("Enter a number: "))
even_odd = input("evensum or oddsum ?: ").lower()
evensum = 0
oddsum = 0

if even_odd == "evensum":
  i = 0
  while i <= num:
    print(i)
    evensum += i
    i+=2
  print("Evensum = ",evensum)
elif even_odd == "oddsum":
  i = 1
  while i <=num:
    print(i)
    oddsum += i
    i+=2
  print("Oddsum = ",oddsum)
else:
  print("Invalid Input")