list1= [1,2,3,4,8]
list2=[1,2,4,5]
list3=[]

for i in range(min(len(list1),len(list2))):
  if list1[i] == list2[i]:
    list3.append(list1[i])
print(list3)