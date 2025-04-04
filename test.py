import random
from constants import *

def draw_graph(f):
    for x in range(13):
        print()
        for y in range(12):
            print(x, end="")

draw_graph(lambda x: x * 1)
