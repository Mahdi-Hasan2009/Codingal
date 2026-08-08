test_dict = input("Enter a dictionary (like: {'Codingal': 3, 'is': 2, 'best': 2, 'for': 2, 'Coding': 1}): ")
new_test_dict = eval(test_dict)


if test_dict == "exit":
    exit()


print("The original dictionary : " + str(new_test_dict))

K = int(input("Enter a value to check frequency: "))

res = 0
for key in new_test_dict:
    if new_test_dict[key] == K:
        res = res +  1
        
        
        
        
print("Frequency of", K, "is :", res)
