import random
from constants import *

class LowerCaseDict(dict):
    def __setitem__(self, key, value):
        key = str(key).lower()
        super().__setitem__(key, value)


lowercasedict = LowerCaseDict({'ONE': 1})
lowercasedict.update({'TWO': 2})

print(lowercasedict)
