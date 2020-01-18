from Car import *


print("\n\nExample 1:")
car1 = Car(0, 0, 2, 1)
car2 = Car(10, 0, -2, 1)

Car.predict_collision(car1, car2)





print("\n\nExample 2:")
car1 = Car(0, 0, 1, 1)
car2 = Car(6, 2, -5, 5)

Car.predict_collision(car1, car2)


