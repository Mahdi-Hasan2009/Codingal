def take_input():
  radius = float(input("Enter your circle's radius: "))
  find_circumference(radius)
def find_circumference(radius):
  y = 3.141592653589793238462643383279502884197169399
  x = 2 * y * radius
  print(f"Your circumference is: {x}")
  
take_input()