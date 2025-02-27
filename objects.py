import random
import pygame
import math
from constants import *

class Rectangle:
    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height

    def contains(self, point):
        px, py = point
        return (self.x <= px <= self.x + self.width and
                self.y <= py <= self.y + self.height)

    def intersects(self, other):
        return not (other.x > self.x + self.width or
                   other.x + other.width < self.x or
                   other.y > self.y + self.height or
                   other.y + other.height < self.y)

class Quadtree:
    def __init__(self, boundary, capacity):
        self.boundary = boundary
        self.capacity = capacity
        self.objects = []
        self.divided = False
        self.northeast = None
        self.northwest = None
        self.southeast = None
        self.southwest = None

    def subdivide(self):
        x, y, w, h = self.boundary.x, self.boundary.y, self.boundary.width, self.boundary.height
        half_w, half_h = w / 2, h / 2

        ne = Rectangle(x + half_w, y, half_w, half_h)
        self.northeast = Quadtree(ne, self.capacity)
        nw = Rectangle(x, y, half_w, half_h)
        self.northwest = Quadtree(nw, self.capacity)
        se = Rectangle(x + half_w, y + half_h, half_w, half_h)
        self.southeast = Quadtree(se, self.capacity)
        sw = Rectangle(x, y + half_h, half_w, half_h)
        self.southwest = Quadtree(sw, self.capacity)

        self.divided = True

    def insert(self, obj):
        if not self.boundary.contains((obj.x, obj.y)):
            return False

        if len(self.objects) < self.capacity:
            self.objects.append(obj)
            return True

        if not self.divided:
            self.subdivide()

        if self.northeast.insert(obj):
            return True
        if self.northwest.insert(obj):
            return True
        if self.southeast.insert(obj):
            return True
        if self.southwest.insert(obj):
            return True

        return False

    def query(self, range, found=None):
        if found is None:
            found = []

        if not self.boundary.intersects(range):
            return found

        for obj in self.objects:
            if range.contains((obj.x, obj.y)):
                found.append(obj)

        if self.divided:
            self.northeast.query(range, found)
            self.northwest.query(range, found)
            self.southeast.query(range, found)
            self.southwest.query(range, found)

        return found
    
    def remove(self, obj):
        """Удаляет объект из квадродерева."""
        if obj in self.objects:
            self.objects.remove(obj)
            return True

        if self.divided:
            if self.northeast.remove(obj):
                return True
            if self.northwest.remove(obj):
                return True
            if self.southeast.remove(obj):
                return True
            if self.southwest.remove(obj):
                return True

        return False
    
# Глобальная переменная для квадродерева
quadtree = Quadtree(Rectangle(0, 0, WIDTH, HEIGHT), capacity=4)

class Body:

    def __init__(self, x, y, color, birthday, energy=100, size=CELL_SIZE, visible=3):
        self.x = x
        self.y = y
        self.color = color
        self.birthday = birthday
        self.energy = energy
        self.size = size
        self.visible = visible
        quadtree.insert(self)

    def update_coordinates(self, new_crd):
        quadtree.remove(self)
        self.x, self.y = new_crd
        quadtree.insert(self)

    def clear_body(self):
        quadtree.remove(self)

    def collision(self):
        range = Rectangle(self.x - self.size, self.y - self.size, self.size * 2, self.size * 2)
        nearby_objects = quadtree.query(range)
        for obj in nearby_objects:
            if obj != self and math.hypot(self.x - obj.x, self.y - obj.y) < (self.size + obj.size):
                print(f"Коллизия между {self.__class__.__name__} и {obj.__class__.__name__}")
                break

    def random_coordinates():
        while True:
            x = random.randint(0, WIDTH)
            y = random.randint(0, HEIGHT)
            return (x, y)

class Grass(Body):
    def __init__(self, x, y, birthday, color=GREEN):
        super().__init__(x, y, color, birthday)

class Predator(Body):
    def __init__(self, x, y, birthday, color=RED):
        super().__init__(x, y, color, birthday)

class Herbivore(Body):
    def __init__(self, x, y, birthday, color=CYAN):
        super().__init__(x, y, color, birthday)

class Player(Body):
    def __init__(self, x, y, birthday, color=BLUE):
        super().__init__(x, y, color, birthday)

    def move_player(self, pressed):
        speed = 1
        if pressed[pygame.K_w]:
            self.update_coordinates((self.x, self.y - speed))
        if pressed[pygame.K_s]:
            self.update_coordinates((self.x, self.y + speed))
        if pressed[pygame.K_a]:
            self.update_coordinates((self.x - speed, self.y))
        if pressed[pygame.K_d]:
            self.update_coordinates((self.x + speed, self.y))
        self.collision()
