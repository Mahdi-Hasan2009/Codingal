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