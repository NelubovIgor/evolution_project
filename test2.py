def polynomial(p):
    result = ''
    for i, s in enumerate(reversed(p)):
        if i == 0 and s != 0:
            if s > 0:
                result += str(s) + "+"
            else:
                result += str(abs(s)) + "-"
        if i == 1 and s != 0:
            if s > 0:
                result += str(s) + "+"
            else:
                result += str(abs(s)) + "-"
    return result

print(polynomial((1, 3, -1, 1, -2)))
