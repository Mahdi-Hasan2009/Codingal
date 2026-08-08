

list1 = [1,2,3,4,8,9,10,1,1]
list2 = [1,2,3,11,12,14,15,18,19,10,19,22,23,4,1]
list3 = []

for i in list1:
    if i in list2 and i not in list3:
        list3.append(i)

print(list3)


