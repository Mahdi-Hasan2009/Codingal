# একটি ক্লাস তৈরি করা
class Student:
    def __init__(self, name, age):
        self.name = name
        self.age = age

    def show_info(self):
        print(f"Name: {self.name}, Age: {self.age}")

# অবজেক্ট তৈরি করা
s1 = Student("Mahdi", 15)
s2 = Student("Arif", 16)

# অবজেক্টের মেথড কল করা
s1.show_info()
s2.show_info()


"""
class Student: → ক্লাসের নাম (Blueprint তৈরি করা)

__init__ → একটা বিশেষ method (constructor), যা object তৈরি হলে প্রথমে চলে

self → সেই নির্দিষ্ট object নিজে

self.name, self.age → object এর ভেতরের ডেটা (attribute)

show_info() → একটি method, যা ডেটা দেখায়

"""


#HW

class Car:
  def __init__(self,brand,model,year):
    self.brand = brand
    self.model = model
    self.year = year
  def  show_info(self): # ***
    print(f"Name:{self.brand},Model:{self.model},Year:{self.year} ")
    

car1 = Car("Toyota","Corolla",2020)
car2 = Car("BMW","R15",2015)

car1.show_info()
car2.brand = "greedy"
"""
🧠 5. Attribute যোগ করা (dynamic attribute)

তুমি চাইলে object-এর পরে নতুন attribute যোগও করতে পারো 
"""
car2.year = 2023 
"""
✏️ 4. Attribute পরিবর্তন (বাইরে থেকে)

তুমি চাইলে object-এর attribute ক্লাসের বাইরে থেকেও পরিবর্তন করতে পারো
"""


car2.show_info()


"""
⚠️ কিন্তু সাবধান:
সবসময় নতুন attribute constructor (__init__) এর মধ্যে ঘোষণা করা ভালো,
এতে কোড পরিষ্কার ও নিয়ন্ত্রিত থাকে।

"""
# class 2 

"""
🔸 Method হলো object-এর ভিতরের ফাংশন যা কোনো কাজ করে।
এগুলো সবসময় self প্যারামিটার নেয় — কারণ method object-এর ভেতরের data ব্যবহার করে।

"""



class Dog:
    species = "Mammal"  # Class attribute

    def __init__(self, name):
        self.name = name  # Instance attribute
        
        
"""
💡 7. তিন ধরণের Attribute :
ধরন	                               অবস্থান	                     অ্যাক্সেস পদ্ধতি
Instance Attribute	                __init__ এর ভিতরে	          self.attribute
Class Attribute	                    ক্লাসের বাইরে, কিন্তু ভিতরে	     ClassName.attribute
Local Variable	                    মেথডের ভিতরে	              শুধু মেথডের ভেতরে
"""

# HW:

class Mobile:
  def __init__(self,brand,model,price):
    self.brand = brand
    self.model = model
    self.price = price
    
  def show_details(self):
    print(f"Brand:{self.brand},Model:{self.model},Price:{self.price}")
  def apply_discount(self,percent):
    self.price = self.price*(1-percent/100)

m1 = Mobile("Samsung","S24",100000)
m1.show_details()
m1.apply_discount(10) # 10% discount
m1.show_details() # ***


# class 3 Encapsulation
"""
🔹 আজ কী শিখব:

Encapsulation কী এবং কেন দরকার

Private attribute (গোপন ডেটা)

Getter & Setter method

Data protection ও নিরাপদ attribute পরিবর্তন


🧠 1. Encapsulation কী?

Encapsulation মানে হলো—

একটি object-এর ডেটা এবং method একসাথে রাখা এবং object-এর ডেটাকে বাইরের থেকে সরাসরি অ্যাক্সেস থেকে রক্ষা করা।
সুবিধা:

✅ ডেটা নিরাপদ থাকে

✅ ভুলভাবে data পরিবর্তনের সম্ভাবনা কমে

✅ কোড maintain করা সহজ হয়

🔹 2. Private Attribute

Python-এ private attribute underscore দিয়ে তৈরি করা হয়:



"""
class BankAccount:
    def __init__(self, balance):
        self.__balance = balance  # private attribute

    def show_balance(self):
        print(f"Balance: {self.__balance}")

account = BankAccount(5000)
#print(account.__balance)  # ❌ Error

"""
⚙️ 3. Getter & Setter Method

Getter → private attribute দেখা
Setter → private attribute update করা (নিরাপদভাবে)


"""


class BankAccount:
    def __init__(self, balance):
        self.__balance = balance

    # Getter
    def get_balance(self):
        return self.__balance

    # Setter
    def deposit(self, amount):
        if amount > 0:
            self.__balance += amount
        else:
            print("Invalid amount")

    def withdraw(self, amount):
        if 0 < amount <= self.__balance:
            self.__balance -= amount
        else:
            print("Insufficient balance or invalid amount")

account = BankAccount(5000)

# সরাসরি access ❌
# print(account.__balance)  # Error

# Getter ব্যবহার ✅
print(account.get_balance())  # 5000

# Deposit/Withdraw ✅
account.deposit(2000)
print(account.get_balance())  # 7000

account.withdraw(3000)
print(account.get_balance())  # 4000



# HW



