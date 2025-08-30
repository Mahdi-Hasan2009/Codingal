 numbers = [2,3,4,5,6,7,8,9]

odd = [i for i in numbers if i%2 == 1 ]
print("List of odd numbers: ",odd)

def cube(x):
  return x*x*x

oddCube = list(map(cube,odd))
print(f"List of oddCube numbers: ",oddCube)


zipped = list(zip(odd,oddCube)) 
print(f"List of zip numbers : ",zipped)

for item in oddCube:
  if item%3 == 0:
    print("Divisible")
  else:
    print("Not Divisible")
    exit()