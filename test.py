import re

text = "Hello, my name is [u-1061][u-1072][u-1082][u-1080]!"

while True:
    indx = text.find('[u-')
    if indx == -1: break
    print(text[0:indx])
    print(chr(int(text[indx+3:indx+7])))
    print(text[indx+8:])
    text = text[0:indx] + chr(int(text[indx+3:indx+7])) + text[indx+8:]

print(text)
