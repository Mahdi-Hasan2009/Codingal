n = "Hello"
for i in n:
  print(i)
print("______________")
for X in n:
  print(X)

print("_____")

for i in range(10):
  print(i)
  
print("_________")
# activity 1

#n = (int(input("Enter a number: ")))#correct but not standard
n = int(input("Enter a number: "))#Standard
#sum = (0)#correct but not standard
sum = 0 #standard

for i in range(1,n+1):
  sum = sum+i
  print("\nSum =",sum)
  
print("_________")
# activity 2

word1 = input("Enter a word to reverse: ")
#word2 = ("")#not standard
word2 = "" #standard


for i in word1:
  word2 = i + word2
print("reverse word : ",word2)
print("_________")
# activity 3

n = int(input("Enter the value of n: "))

print("numbers from {} to {} are: ".format(n,1))#better
#print("numbers from {0} to {1} are: ".format(n,1)) #not better

for i in range(n,0,-1):
  print(i)



# my activity 

n = int(input("Enter a number for table: "))

for i in range(1,11):
  print(n,"*" ,i, "=", n*i)
    
    # my activity 


n = int(input("Enter n: "))
sum = 0

for i in range(1, n + 1):
    sum += i

average = sum / n
print("Sum =", sum)
print("Average =", average)

# my activity 

n = int(input("Enter a number for average: "))
sum = 0
for i in range(1,n+1):
  sum+=i   #*************
print("average: ",sum/n)
# my activity 

n = int(input("Enter a number for even number: "))

for i in range(2,n+1,2):
  print(i,end=" ")
# my activity 

n = int(input("Enter a number for odd number: "))

for i in range(1,n+1,2):
  print(i,end=" ")
  
# my activity 
word = input("Enter a word: ")
vowel_count = 0

for ch in word:
    if ch.lower() in "aeiou":
        vowel_count += 1

print("Vowel count:", vowel_count)

# my activity 

word = input("Enter a word: ")
count_vowel = 0
for ch in word:
  if ch.lower() in "aeiou":# remember "in"
     count_vowel+=1
print("Total vowel: ", count_vowel)

#same

word = input("Enter a word: ")
count_vowel = 0
for ch in word:
  if ch.lower() in ["a","e","i","o","u"]:# remember "in"
     count_vowel+=1
print("Total vowel: ", count_vowel)


# my activity 

num = int(input("Enter a number for factorial: "))
fact = 1

for i in range(1,num+1):
  fact*=i
print("Factorial of your number is: ",fact)
# my activity 

n = int(input("Enter a number: "))
is_prime = True

if n < 2:
    is_prime = False
else:
    for i in range(2, n):
        if n % i == 0:
            is_prime = False
            break

if is_prime==True:
    print(n, "is a prime number.")
else:
    print(n, "is not a prime number.")
    
# my activity 
n= int(input("Enter a number: "))
is_prime = True
if n<2:
  is_prime= False
else:
  for i in range(2,n):
    if n %i==0:
      is_prime=False
      break
if is_prime:
  print(n,"is a prime number")
else:
  print(n,"is not a prime number")

# my activity 

#12/24 = 0.5
#12%24 = 2  or 24/12 = 2
a = 20
b = 30

def gcd(a,b):
    while b!=0:
        a,b = b,a%b
    return a
def lcm(a,b):
    return a*b //gcd(a,b)

print("GCD: ",gcd(a,b))
print("LCM: ",lcm(a,b))


# my activity 


#12/5 = 2.4
#12//5 = 2
    
a = int(input("Enter a number: "))
b = int(input("Enter a number: "))
def gcd(a,b):
    while b!=0:
        a,b = b,a%b
    return a
def lcm(a,b):
    return a*b // gcd(a,b)

same_day = lcm(a,b)
a_cycle = same_day//a 
b_cycle = same_day//b 

print("Same-day cycle after:", same_day, "days")
print("A completes:", a_cycle, "cycles")
print("B completes:", b_cycle, "cycles")

# my activity 

Rahim_jog_day = 8
karim_jog_day = 12
 
def gcd(a,b):
    while b!=0:
        a,b = b,a%b
    return a
def lcm(a,b):
    return a*b // gcd(a,b)

result = lcm(Rahim_jog_day,karim_jog_day)

print("Rahim ও Karim একসাথে আবার", result, "দিন পরে jogging করবে।")

# my activity

def gcd(a,b):
    while b!=0:
        a,b = b,a%b
    return a

def lcm(a,b):
    return a*b //gcd(a,b)
bus1 = 9
bus2= 15
result = lcm(bus1,bus2)

print("They will arrive together after ",result,"times")

# my activity

n = int(input("Enter the number whose sum you want to find: "))
sum = 0

for i in range(1,n+1):
  sum = sum+i
  print("\nsum=",sum)

