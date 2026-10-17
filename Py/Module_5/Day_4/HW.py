class Vehicle:
  def __init__(self, name, capacity):
    self.name = name
    self.capacity = capacity
    
  def display(self):
    return self.capacity * 100
  
class Bus(Vehicle):
  def fare(self):
    amount = super().display()
    amount += amount * 10 / 100
    return amount

bus = Bus("Volvo", 50)
print("Total Bus fare is:", bus.fare())