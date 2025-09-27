#parent class
class Person(object):
  
  #__init__ known as constructor
  
  def __init__(self,name,id_number):
    self.name = name
    self.id_number = id_number
    
  def display(self):
    print(self.name)
    print(self.id_number)
    
    
#child class
class Employee(Person):
  def __init__(self,name,id_number,salary,post):
    super().__init__(name,id_number)
    self.salary = salary
    self.post = post
    
  def display(self):
    print(self.name)
    print(self.id_number)
    print(self.salary)
    print(self.post)
    
    
# creation of an object variable or an instance

a = Employee("Muhtadi",886012,200000,"Intern")

# calling a function of the class Person using its instance

a.display()



    