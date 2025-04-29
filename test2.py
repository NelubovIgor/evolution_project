def snake(n):
    print()

# snake(3)


def mystery(n):
    donats = 0
    for s in str(n):
        if s == "6" or s == "9" or s == "0": donats += 1
        elif s == "8": donats += 2    
    return donats

print(mystery(88600))
