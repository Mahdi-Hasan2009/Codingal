class fruit:
  print("hey this is an example of classes and objects")

ob = fruit()# ***** 
hello = fruit()# no problem  


#____________________________


class fruit:
  #Constructor
  def __init__(self,name,color):
    self.name = name # self is an instant variable  so we can use it outside of class attribute
    self.color = color

# object creation

apple = fruit("Apple","Red")# *****
print(apple.name)


#____________________________


class check:
  def __init__(self):
    print("Address of self = ",id(self))
    
obj = check()
print("Address of object = ",id(obj))




#____________________________












