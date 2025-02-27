import random, pygame, math
from constants import *


class SpatialHash:
    def __init__(self, cell_size):
        self.cell_size = cell_size
        self.grid = {}

    def _get_cell_key(self, x, y):
        return (int(x // self.cell_size), int(y // self.cell_size))

    def insert(self, obj):
        # Определяем ячейки, с которыми пересекается объект
        min_x = obj.x - obj.size
        max_x = obj.x + obj.size
        min_y = obj.y - obj.size
        max_y = obj.y + obj.size

        for x in range(int(min_x // self.cell_size), int(max_x // self.cell_size) + 1):
            for y in range(int(min_y // self.cell_size), int(max_y // self.cell_size) + 1):
                key = (x, y)
                if key not in self.grid:
                    self.grid[key] = []
                self.grid[key].append(obj)

    def query(self, x, y, radius):
        # Находим объекты в ячейках, с которыми пересекается область
        min_x = x - radius
        max_x = x + radius
        min_y = y - radius
        max_y = y + radius

        result = []
        for x_cell in range(int(min_x // self.cell_size), int(max_x // self.cell_size) + 1):
            for y_cell in range(int(min_y // self.cell_size), int(max_y // self.cell_size) + 1):
                key = (x_cell, y_cell)
                if key in self.grid:
                    result.extend(self.grid[key])
        return result

    def remove(self, obj):
        min_x = obj.x - obj.size
        max_x = obj.x + obj.size
        min_y = obj.y - obj.size
        max_y = obj.y + obj.size

        for x in range(int(min_x // self.cell_size), int(max_x // self.cell_size) + 1):
            for y in range(int(min_y // self.cell_size), int(max_y // self.cell_size) + 1):
                key = (x, y)
                if key in self.grid and obj in self.grid[key]:
                    self.grid[key].remove(obj)

spatial_hash = SpatialHash(cell_size=50)

class Body:


    def __init__(self, x, y, color, birthday, energy=100, size=CELL_SIZE, visible=3):
        self.x = x
        self.y = y
        self.color = color
        self.birthday = birthday
        self.energy = energy
        self.size = size
        self.visible = visible

        spatial_hash.insert(self)

    def update_coordinates(self, new_crd):
        spatial_hash.remove(self)
        self.x, self.y = new_crd
        spatial_hash.insert(self)

    def touch(self):
        pass

    def vision(self):
        pass

    def move(self):
        pass

    def clear_body(self):
        spatial_hash.remove(self)

    def random_coordinates():
        while True:
            x = random.randint(0, WIDTH)
            y = random.randint(0, HEIGHT)
            # if (x, y) not in Body.all_bodies:
            #     return x, y
            
    def collision(self):
        nearby_objects = spatial_hash.query(self.x, self.y, self.size)
        for obj in nearby_objects:
            if obj != self and math.hypot(self.x - obj.x, self.y - obj.y) < (self.size + obj.size):
                print(f"Коллизия между {self.__class__.__name__} и {obj.__class__.__name__}")
                break


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
            self.update_coordinates(self, (self.x, self.y - speed))
            self.y -= speed
        if pressed[pygame.K_s]:
            self.update_coordinates(self, (self.x, self.y + speed))
            self.y += speed
        if pressed[pygame.K_a]:
            self.update_coordinates(self, (self.x - speed, self.y))
            self.x -= speed
        if pressed[pygame.K_d]:
            self.update_coordinates(self, (self.x + speed, self.y))
            self.x += speed
        self.collision(self)
