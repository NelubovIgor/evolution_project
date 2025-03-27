import random
from constants import *
from abc import ABC, abstractmethod

class AbstractClass(ABC):
    @abstractmethod
    def method(self):
        return 1


obj = AbstractClass()

print(obj.method())
