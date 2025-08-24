
test_dict = input("Enter a tuple (like: (1, 2, 3)): ")

new_test_dict = eval(test_dict)

while test_dict == "exit":
  break 

print("The original dictionary : " + str(test_dict))


K = int(input("Enter a key: "))

res = 0

for key in test_dict:
  if test_dict[key] == K:
    res = res +1
    
    
print("Frequency of K is : " + str(res))