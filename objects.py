import random, pygame, math
from constants import *
import copy

class World:
    def __init__(self):
        self.bodies = {}

    def world_life(self):
        copy_world = copy.copy(self)
        for coord, obj in world.bodies.items():
            if isinstance(obj, Animal):
                Animal.do(obj)
            elif isinstance(obj, Grass):
                pass

    def add_body(self, obj):
        if (obj.x, obj.y) not in self.bodies:
            self.bodies[(obj.x, obj.y)] = obj

    def random_coordinates(self):
        while True:
            x = random.randint(0, WIDTH)
            y = random.randint(0, HEIGHT)
            if (x, y) not in self.bodies:
                return x, y
            
    def clear_body(self, obj):
        del self.bodies[(obj.x, obj.y)]

    def update_coordinates(self, obj, old_obj):
        self.clear_body(old_obj)
        self.add_body(obj)

    def collision(self):
        pass


class Body:
    def __init__(self, x, y, color, birthday, energy=100, size=CELL_SIZE, visible=3):
        self.x = x
        self.y = y
        self.color = color
        self.birthday = birthday
        self.energy = energy
        self.size = size
        self.visible = visible
        self.memory = []


    def vision(self, visible=1):
        objects = []

        min_x = 0 if self.x - visible < 0 else self.x - visible
        max_x = WIDTH if self.x + visible > WIDTH else self.x + visible
        min_y = 0 if self.y - visible < 0 else self.y - visible
        max_y = HEIGHT if self.x + visible > HEIGHT else self.x + visible

        for x in range(min_x, max_x):
            for y in range(min_y, max_y):
                if x == self.x and y == self.y:
                    continue
                elif (x, y) in world.bodies:
                    objects.append(world.bodies[(x, y)])
        
        return objects


    def move(self, target, to_target=True):
        pass

    def reproduction():
        pass

    def sleep(self):
        pass

class Animal(Body):
    def __init__(self, x, y, birthday, color):
        super().__init__(x, y, color, birthday)

    def do(self):
        self.energy -= 0.1

        touch = self.vision()
        if not touch:
            obj = self.vision(self.visible)
        else:
            obj = touch

class Grass(Body):
    def __init__(self, x, y, birthday, color=GREEN):
        super().__init__(x, y, color, birthday)

class Predator(Animal):
    def __init__(self, x, y, birthday, color=RED):
        super().__init__(x, y, color, birthday)

class Herbivore(Animal):
    def __init__(self, x, y, birthday, color=CYAN):
        super().__init__(x, y, color, birthday)

class Player(Body):
    def __init__(self, x, y, birthday, color=BLUE):
        super().__init__(x, y, color, birthday)

    def move_player(self, pressed):
        copy_obj = copy.copy(self)
        speed = 1
        if pressed[pygame.K_w]:
            # self.update_coordinates((self.x, self.y - speed))
            self.y -= speed
        if pressed[pygame.K_s]:
            # world.update_coordinates(self)
            self.y += speed
        if pressed[pygame.K_a]:
            # world.update_coordinates(self)
            self.x -= speed
        if pressed[pygame.K_d]:
            # world.update_coordinates(self)
            self.x += speed
        world.update_coordinates(self, copy_obj)

cycle = 0

world = World()

# создание объектов
player1 = Player(200, 200, cycle)
world.add_body(player1)

food = (Grass(21, 20, cycle))
world.add_body(food)

bot = (Herbivore(20, 20, cycle))
world.add_body(bot)

def make_objects():
    for _ in range(20):
        x, y = world.random_coordinates()
        g = Grass(x, y, cycle)
        world.add_body(g)

    for _ in range(5):
        x, y = world.random_coordinates()
        p = Predator(x, y, cycle)
        world.add_body(p)
