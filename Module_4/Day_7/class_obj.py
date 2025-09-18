class car:
  #brand mileage color
  # obj 2 mercedes bmw
  #species = "car"
  species = "car"
  
  def __init__(self,brand,mileage,color):
    self.brand = brand
    self.mileage = mileage
    self.color = color
    
mercedes = car("mercedes",8786,"red")
bmw = car("bmw",585,"blue")


print(mercedes.brand , mercedes.color)
print(bmw.mileage)