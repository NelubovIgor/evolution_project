import random
from constants import *

a = 40
b = 39

# print(b * HEIGHT + a)
# print(a * HEIGHT + b)

c = 0 if a - b <= 0 else a - b

dir_x = 2
dir_y = 0

to_x = int(dir_x / dir_x) if dir_x > 0 else int((dir_x / dir_x) * -1)

if dir_y != 0:
    to_y = int(dir_y / dir_y) if dir_y > 0 else int((dir_y / dir_y) * -1)
else:
    to_y = 0
    
print(to_y)

# print(c)
