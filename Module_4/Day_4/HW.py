set1 = {"blue","green"}
set2 = {"blue","yellow"}

difference1 = set1.symmetric_difference(set2)
test_difference = set2.symmetric_difference(set1)
print(difference1)
print(test_difference)


set3 = {1,2,3,4,5}
set4 = {1,5,6,7,8,9}

difference2 = set3.symmetric_difference(set4)
print(difference2)