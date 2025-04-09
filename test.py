import random
from constants import *

def draw_graph(f):
    for y in range(12):
        print()
        for x in range(13):
            if x == 0:
                if y == 0:
                    print('y', end="")
                elif 0 < y < 10:
                    print(10 - y, end="")
                else:
                    print(' ', end="")
            elif x == 1:
                if y == 0:
                    print(' ^ ', end="")
                elif 0 < y < 10:
                    print(' | ', end="")
                elif y == 10:
                    print(' +-', end="")
                else:
                    print('   ', end="")
            elif y == 10:
                if 1 < x < 10:
                    print('---', end="")
                elif x == 10:
                    print('--', end="")
                elif x == 11:
                    print(' >', end="")
                elif x == 12:
                    print(' x', end="")
            elif y == 11:
                if 1 < x < 11:
                    print(f" {x - 1} ", end="")
            elif 1 < x < 11 and 0 < y < 10:
                point_x = f(x-1)
                point_y = 10 - y
                if point_x == point_y:
                    print(' * ', end="")

def draw_graph1(f):
    for y in range(12):
        print()
        for x in range(13):
            point_x = f(x)
            point_y = f(y)
            print(point_x, point_y)

# draw_graph1(lambda x: 2)
# draw_graph(lambda x: x * 1)

def equation_of_line(values):
    k = (1 - 0) / (values[0] - values[1])
    b = (0 * values[1] - values[0] * 1) / (values[0] - values[1])
    for y, x in enumerate(values):
        if y < 2:
            continue
        return float(y) == k * x + b

print(equation_of_line([0, 1, 2, 3, 4]))
