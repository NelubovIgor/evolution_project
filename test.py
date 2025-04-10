import random, math
from constants import *

def quadratic_intersections(a1, b1, c1, a2, b2, c2):
    points = set()
    a = a1 - a2
    b = b1 - b2
    c = c1 - c2
    d = b ** 2 - 4 * a * c
    x1 = None
    x2 = None
    if d >= 0 and a != 0:
        x1 = (-b - math.sqrt(d)) / (2 * a)
        if d > 0:
            x2 = (-b + math.sqrt(d)) / (2 * a)
    if x1 != None:
        y1 = a1 * x1 ** 2 + b1 * x1 + c1
        points.add((x1, y1))
        if x2 != None:
            y2 = a2 * x2 ** 2 + b2 * x2 + c2
            points.add((x2, y2))
    if a == 0 and b != 0:
        x = -(c / b)
        y = a * x ** 2 + b * x + c
        points.add((x, y))
    return points

# print(quadratic_intersections(1, 2, 3, 1, 1, 4))

d = 2024 ** 2 - 4 * 1 * -2025
print((2024 + d ** 0.5) / 2 * 1)