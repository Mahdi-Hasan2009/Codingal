class BMW:
    def fuel_type(self):
        return "Petrol"

    def max_speed(self):
        return "240 km/h"

class Ferrari:
    def fuel_type(self):
        return "Petrol (High Octane)"

    def max_speed(self):
        return "340 km/h"



cars = [BMW(), Ferrari()]

for car in cars:
    print(f"{car.__class__.__name__} Fuel Type:", car.fuel_type())
    print(f"{car.__class__.__name__} Max Speed:", car.max_speed())