import random, math, itertools
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

def polynomial_sum(p1, p2):
    pp = {}
    result = list()
    def intermediate_result(p):
        for i, n in enumerate(reversed(p)):
            if i not in pp:
                pp[i] = n
            else:
                pp[i] += n
    intermediate_result(p1)
    intermediate_result(p2)
    # print(pp)
    for degree, num in pp.items():
        # if (degree == 0 or degree == 1) and num == 0:
        #     continue

        result.append(num)

    return tuple(reversed(result))

p1 = (2, -4, 5)                  # P1(x) = 2x^2 - 4x + 5
p2 = (3, 2)                      # P2(x) = 3x + 2

print(polynomial_sum(p1, p2))    # P1(x) + P2(x) = 2x^2 - x + 7

p1 = (1, 7, 0, -4)               # P1(x) = x^3 + 7x^2 - 4
p2 = (-1, 0, 0, 2)               # P2(x) = -x^3 + 2

print(polynomial_sum(p1, p2))    # P1(x) + P2(x) = 7x^2 - 2

p1 = (1, 2, 3, 4, 5)             # P1(x) = x^4 + 2x^3 + 3x^2 + 4x + 5
p2 = (1,)                        # P2(x) = 1

print(polynomial_sum(p1, p2))    # P1(x) + P2(x) = x^4 + 2x^3 + 3x^2 + 4x + 6

p1 = (1, 1, 1, 1)                # P1(x) = x^3 + x^2 + x + 1
p2 = (-1, -1, -1, -1, -1)        # P2(x) = -x^4 - x^3 - x^2 - x - 1

print(polynomial_sum(p1, p2))    # P1(x) + P2(x) = -x^4

nums = [(1-(1/n**2)) for n in range(2, 11)]
result = 1
for n in nums:
    result *= n
print(result)    
