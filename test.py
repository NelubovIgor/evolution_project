import random
from constants import *

num = 12
while True:
    answer_num = int('2' + str(num)[1:-1])
    print(num)
    if num * 2 == answer_num:
        print(answer_num) 
        break
    num += 10

# print(str(num)[1:-1])
