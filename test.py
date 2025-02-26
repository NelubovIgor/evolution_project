author = ''
book = ''
flag = "YES"

for _ in range(int(input())):
    string = input()
    a = string[:string.find(" ")]
    b = string[string.rfind(" "):]
    if author >= a and book >= b:
        author = a
        book = b
    else:
        flag = "NO"
        break

print(flag)