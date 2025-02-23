n = "А1_23ОВ_45"

lit = 'АВЕКМНОРСТУХ'
num = n.split('_')
if len(num) == 2:
    if len(num[0]) == 6 and (2 <= len(num[1]) <= 3):
        if num[0][0] in lit and num[0][1:4].isdigit() and num[0][4] in lit and num[0][5] in lit and num[1].isdigit():
            print("YES")
        else:
            print("NO")
    else:
        print("NO")
else:
    print("NO")