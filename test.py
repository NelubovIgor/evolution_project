import random
from constants import *

class Triangle:
    def __init__(self, a, b, c):
        self.a = a
        self.b = b
        self.c = c
    
    def perimeter(self):
        return self.a + self.b + self.c

class EquilateralTriangle(Triangle):
    def __init__(self, side):
        super().__init__(side, side, side)
        self.a = side
        self.b = side
        self.c = side


triangle1 = Triangle(3, 4, 5)
triangle2 = EquilateralTriangle(3)

print(triangle1.perimeter())
print(triangle2.perimeter())   


# print(tuple(a + b for a, b in zip(random.choice(list(DIRECTIONS.values())), (30, 34))))
