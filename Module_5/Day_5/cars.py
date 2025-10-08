from abc import ABC,abstractmethod

class Car(ABC):
  def __init__(self,wheels):
    self.wheels = wheels
  
  def specialFeatures(self):
    pass
class Toyota(Car):
  def __init__(self,wheels,color,mileage):
    super().__init__(wheels)
    self.color = color
    self.mileage = mileage
    
  def specialFeatures(self):
    print("Highest Mileage")

class BMW(Car):
  def __init__(self,wheels,color,mileage):
    super().__init__(wheels)
    self.color = color
    self.mileage = mileage
    
  def specialFeatures(self):
    print("Lowest Mileage")

  
obj1 = Toyota(4,"white",100)
print(obj1.color)
obj1.specialFeatures()
  
