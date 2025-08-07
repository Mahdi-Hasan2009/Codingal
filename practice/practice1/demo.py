def is_prime(n):
    if n < 2:
        return False
    for i in range(2, n):
        if n % i == 0:
            return False
    return True

smallnum = int(input("Enter the smaller number: "))
largenum = int(input("Enter the larger number: "))

for num in range(smallnum, largenum + 1):
    if is_prime(num):
        print(num)
    else:
        pass  
        







    







