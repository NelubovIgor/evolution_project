import random, math, itertools
from constants import *

def intersections(a, b, c, k, m):
    points = list()
    bk = b - k
    cm = c - m
    d = bk ** 2 - 4 * a * cm
    x1 = None
    x2 = None
    if d >= 0 and a != 0:
        if d == 0:
            x3 = -bk / (2 * a)
            y3 = a * x3 ** 2 + bk * x3 + cm
            points.append((x3, y3))
        elif d > 0:
            x1 = (-bk + math.sqrt(d)) / (2 * a)
            y1 = a * x1 ** 2 + bk * x1 + cm
            points.append((x1, y1))
            x2 = (-bk - math.sqrt(d)) / (2 * a)
            y2 = a * x2 ** 2 + bk * x2 + cm
            points.append((x2, y2))
    if a == 0:
        x = -cm / bk
        y = a * x ** 2 + bk * x + cm
        points.append((x, y))
    return set(points)

# print(intersections(1, 0, 0, 1, 0)) #{(0.0, 0.0), (1.0, 1.0)}
# print(intersections(1, -3, 2, 1, -1)) #{(1.0, 0.0), (3.0, 2.0)}


def polynomial_sum(p1, p2):
    p_degree = {k: v for k, v in enumerate(reversed(p1))}
    for k, v in enumerate(reversed(p2)):
        if k in p_degree.items(): p_degree[k] += v
        else: p_degree[k] = v
        
    # p2_degree = {k: v for k, v in enumerate(reversed(p2))}
    # result = list()
    # ren = len(p1_degree) if len(p1_degree) > len(p2_degree) else len(p2_degree)
    # for i in range(ren):
    #     first = p1_degree.get(i, 0)
    #     second = p2_degree.get(i, 0)
    #     if first == 0 and second == 0: continue
    #     result.append(first + second)
    # final = list()



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


def time_zone(h, a, b):
    difference = 0
    if a > b: difference = a - b
    elif a < b: difference = b - a
    if difference == h: return 0
    else: difference += h
    if 24 > difference: return difference
    else: return difference % 24

# print(time_zone(12, 3, 7))
# print(time_zone(6, -11, 12))
# print(time_zone(23, 12, -11))
# print(time_zone(11, 12, -11))
