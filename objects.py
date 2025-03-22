import random, pygame, math
from constants import *
import copy

class World:
    def __init__(self):
        self.bodies = {}
        self.id_to_coords = {}
        self.next_id = 0

    def world_life(self):
        copy_world = copy.deepcopy(self.bodies)
        for coord, obj in self.bodies.items():
            if isinstance(obj, Animal):
                obj.do()
            elif isinstance(obj, Grass):
                pass

    def new_body(self, obj):
        obj.id = self.next_id
        self.next_id += 1
        self.add_body(obj)

    def add_body(self, obj):
        self.bodies[(obj.x, obj.y)] = obj
        self.id_to_coords[obj.id] = (obj.x, obj.y)

    def random_coordinates(self):
        while True:
            x = random.randint(0, WIDTH)
            y = random.randint(0, HEIGHT)
            if (x, y) not in self.bodies:
                return x, y
            
    def clear_body(self, obj):
        del self.bodies[(obj.x, obj.y)]
        del self.id_to_coords[obj.id]

    def update_coordinates(self, obj, old_obj):
        self.clear_body(old_obj)
        self.add_body(obj)

    def collision(self):
        pass


class Body:
    objects_around = []
    
    def __init__(self, x, y, color, birthday, energy=100, size=CELL_SIZE, visible=3):
        self.x = x
        self.y = y
        self.color = color
        self.birthday = birthday
        self.energy = energy
        self.size = size
        self.visible = visible
        self.memory = []
        self.id = None


    def vision(self, visible=1):
        objects_around = []

        min_x = 0 if self.x - visible < 0 else self.x - visible
        max_x = WIDTH if self.x + visible > WIDTH else self.x + visible
        min_y = 0 if self.y - visible < 0 else self.y - visible
        max_y = HEIGHT if self.x + visible > HEIGHT else self.x + visible

        for x in range(min_x, max_x):
            for y in range(min_y, max_y):
                if not (x == self.x and y == self.y) and (x, y) in world.bodies:
                    obj = copy.copy(world.bodies[(x, y)])
                    objects_around.append(obj)

        print(objects_around, self.__class__.__name__, self.id)
        return objects_around
    
    def do(self):
        self.energy -= 0.1

        touch = self.vision()
        print(touch)
        if not touch:
            obj = self.vision(self.visible)
        else:
            obj = touch

    def move(self, target, to_target=True):
        pass

    def reproduction():
        pass

    def sleep(self):
        pass

class Animal(Body):
    def __init__(self, x, y, birthday, color):
        super().__init__(x, y, birthday, color)

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
            self.y -= speed
        if pressed[pygame.K_s]:
            self.y += speed
        if pressed[pygame.K_a]:
            self.x -= speed
        if pressed[pygame.K_d]:
            self.x += speed
        world.update_coordinates(self, copy_obj)

cycle = 0

world = World()
play = False

# создание объектов
if play:
    player1 = Player(200, 200, cycle)
    world.new_body(player1)
else:
    player1 = None

food = (Grass(21, 20, cycle))
world.new_body(food)

# food = (Grass(34, 20, cycle))
# world.add_body(food)

# bot = (Herbivore(20, 20, cycle))
# world.add_body(bot)

bot = (Herbivore(20, 20, cycle))
world.new_body(bot)

def make_objects():
    for _ in range(20):
        x, y = world.random_coordinates()
        g = Grass(x, y, cycle)
        world.new_body(g)

    for _ in range(5):
        x, y = world.random_coordinates()
        p = Predator(x, y, cycle)
        world.new_body(p)
