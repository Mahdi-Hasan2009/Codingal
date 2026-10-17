import math  

class Circle:
    
    def __init__(self, radius):
        self.radius = radius

    
    def area(self):
        return math.pi * (self.radius ** 2)

    
    def perimeter(self):
        return 2 * math.pi * self.radius



r = float(input("Enter the radius of the circle: "))


c1 = Circle(r)


print("Area of Circle:", c1.area())
print("Perimeter of Circle:", c1.perimeter())
