class Dog:
  def __init__(self,breed,age):
    # breed = self.breed not correct
    self.breed = breed
    self.age = age
  def bark(self): # important for line 6 -7
    print("Woof! I am a {0}, and I am {1} years old".format(self.breed,self.age))
    
    
dog1 = Dog("bulldog","10")
dog2 = Dog("German Shepherd","11")

# dog1.bark(self)  using "self" incorrect here
dog1.bark()
dog2.bark()

# step 2
# 📌 Step 2: Encapsulation (Private Variable + Getter & Setter)
"""
Encapsulation মানে হলো ডেটা লুকানো (hide) এবং control করা কিভাবে access করা হবে।
Python-এ আমরা এটা করি private variable দিয়ে (যেটা __ দিয়ে শুরু হয়)। """

# code 

"""❓ তাহলে parameter হিসেবে কেন নেই (__init__(self, maxprice)) ?

যদি চাইতাম ইউজার অবজেক্ট বানানোর সময় দাম ঠিক করুক, তাহলে parameter দিতে হতো। যেমন:

class Computer:
    def __init__(self, maxprice):
        self.__maxprice = maxprice

c1 = Computer(1200)
c2 = Computer(800)


এখন c1 এর দাম হবে 1200, আর c2 এর দাম হবে 800।

কিন্তু তোমার দেওয়া কোডে constructor-এ কোনো parameter দেওয়া হয়নি।
তাই এখানে __maxprice সবসময় default 900 দিয়েই তৈরি হবে।"""

"""class fruit:
  pass
"""

"""
class fruit:
  print("hey! this is an example of class and objects")
  
#Object Creation
ob = fruit() """

class student:
  grade = 10
  print("Hi I am a student of grade",grade)
  
ob = student()

class Vehicles:
  # create init method
  def __init__(self,max_speed,mileage):
    self.max_speed = max_speed
    self.mileage = mileage
    
# object creation
modelX = Vehicles(240,18)

# access the variables inside init method
print("model Max Speed:",modelX.max_speed)
print("model Mileage:",modelX.mileage)

# activity 3


# create class
class Parrot:
  
  # class attribute
  species = "bird"#optional
  
  # instance attribute
  def __init__(self,name,age):
    self.name = name
    self.age = age
    
# instantiate the Parrot class
blu = Parrot("Blu",10)
woo = Parrot("Woo",15)

#access the class attributes
print("Blu is a {}".format(blu.species))
print("Woo is also a {}".format(woo.species))
#access the instance attributes
print("{} is {} years old".format(blu.name,blu.age))
print("{} is {} years old".format(woo.name,woo.age))



# Encapsulation and Special Functions




# create class
class Parrot:
  
  # class attribute #private attribute
  __species = "bird"#optional
  
  # instance attribute # private instance attribute
  def __init__(self,name,age):
    self.__name = name
    self.__age = age
    
    
    
  def __display(self): # private method
    print("this is private method.")
    
    
  std = Parrot("woo",25)
  print(std) # output <__main__.Parrot object at 0x000002AD431A78C0> 

std = Parrot("woo",25)
print(std) # output <__main__.Parrot object at 0x000002AD431A78C0>   

