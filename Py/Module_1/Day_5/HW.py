'''x must be even and lie between 50 and 100, but not divisible by 5.'''

for i in range (50,101):
  if i%2 == 0 and i%5 != 0 :
    print(i)
    
'''
temperature = float(input("Enter a Temperature: "))

if temperature<20:
  print("Wear Jacket")
elif temperature>=20:     # *********  >=
  print("Wear Light Cloth")

'''