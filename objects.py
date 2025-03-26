import random, pygame, math
from constants import *
import copy

class World:
    def __init__(self):
        self.bodies = {}
        self.id_to_coords = {}
        self.next_id = 0

    def world_life(self):
        copy_world = copy.copy(self.bodies)
        for coord, obj in copy_world.items():
            if isinstance(obj, Animal):
                obj.do()
            elif isinstance(obj, Grass):
                obj.grow()
            
    def new_body(self, obj):
        obj.id = self.next_id
        self.next_id += 1
        self.add_body(obj)
        print(len(self.bodies))

    def add_body(self, obj):
        self.bodies[(obj.x, obj.y)] = obj
        self.id_to_coords[obj.id] = (obj.x, obj.y)

    def random_coordinates(self):
        while True:
            x = random.randint(0, WIDTH)
            y = random.randint(0, HEIGHT)
            if (x, y) not in self.bodies:
                return x, y
            
    def borders(obj):
        visible = obj.visible
        min_x = 0 if obj.x - visible < 0 else obj.x - visible
        max_x = WIDTH if obj.x + visible > WIDTH else obj.x + visible + 1
        min_y = 0 if obj.y - visible < 0 else obj.y - visible
        max_y = HEIGHT if obj.y + visible > HEIGHT else obj.y + visible + 1
        return min_x, max_x, min_y, max_y

    def clear_body(self, obj):
        del self.bodies[(obj.x, obj.y)]
        del self.id_to_coords[obj.id]

    def update_coordinates(self, obj, old_obj):
        self.clear_body(old_obj)
        self.add_body(obj)

    def collision(self, obj, target):
        distance = math.hypot((target.x - obj.x) ** 2 + (target.y - obj.y) ** 2)
        radius_sum = obj.size + target.size

        if distance <= radius_sum:
            self.clear_body(target)
            return True
        return False

class Body:
    def __init__(self, x, y, birthday, color, energy=50, size=CELL_SIZE, visible=10, speed=1):
        self.x = x
        self.y = y
        self.color = color
        self.birthday = birthday
        self.energy = energy
        self.size = size
        self.visible = visible
        self.memory = []
        self.genome = []
        self.speed = speed
        self.id = None

    def vision(self, visible=1):
        objects_around = []

        min_x, max_x, min_y, max_y = World.borders(self)

        for x in range(min_x, max_x):
            for y in range(min_y, max_y):
                if x == self.x and y == self.y:
                    continue
                if (x, y) in world.bodies:
                    objects_around.append(world.bodies[(x, y)])
        return objects_around
    
    def reproduction(self, place):
        self.energy /= 2
        if isinstance(self, Animal):
            world.new_body(Animal(place[0], place[1], cycle, energy=self.energy))
        elif isinstance(self, Grass):

            world.new_body(Grass(place[0], place[1], cycle, energy=self.energy))

    def sleep(self):
        pass

class Animal(Body):
    def __init__(self, x, y, birthday, color):
        super().__init__(x, y, birthday, color)

    def do(self):
        self.energy -= 0.1

        obj = self.vision()
        if not obj:
            obj = self.vision(self.visible)
        if not obj:
            self.sleep()
            return
        
        copy_obj = copy.copy(self)

        target = random.choice(obj)
        self.move(target)
        world.collision(self, target)
        world.update_coordinates(self, copy_obj)
        
    def move(self, target, to_target=True):
        
        dir_x = target.x - self.x
        dir_y = target.y - self.y

        if dir_x != 0:
            to_x = int(dir_x / dir_x) if dir_x > 0 else int((dir_x / dir_x) * -1)
        else:
            to_x = 0

        if dir_y != 0:
            to_y = int(dir_y / dir_y) if dir_y > 0 else int((dir_y / dir_y) * -1)
        else:
            to_y = 0

        self.x += to_x
        self.y += to_y


class Grass(Body):
    def __init__(self, x, y, birthday, color=GREEN, energy=100):
        super().__init__(x, y, birthday, color, energy)

    def grow(self):
        self.energy += 1

        if self.energy >= 100:
            min_x, max_x, min_y, max_y = World.borders(self)
            count_step = 0
            while count_step < 10:
                count_step += 1
                x = random.randint(min_x, max_x)
                y = random.randint(min_y, max_y)
                if (x, y) not in world.bodies:
                    self.reproduction((x, y))
                    break


class Predator(Animal):
    def __init__(self, x, y, birthday, color=RED):
        super().__init__(x, y, birthday, color)

class Herbivore(Animal):
    def __init__(self, x, y, birthday, color=CYAN):
        super().__init__(x, y, birthday, color)

class Player(Body):
    def __init__(self, x, y, birthday, color=BLUE):
        super().__init__(x, y, birthday, color)

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

# food = (Grass(20, 21, cycle))
# world.new_body(food)

food1 = (Grass(21, 20, cycle))
world.new_body(food1)

# food2 = (Grass(21, 21, cycle))
# world.new_body(food2)

food = (Grass(34, 20, cycle))
world.new_body(food)

food3 = (Grass(44, 20, cycle))
world.new_body(food3)

food4 = (Grass(54, 20, cycle))
world.new_body(food4)

# bot = (Herbivore(20, 20, cycle))
# world.new_body(bot)

bot = (Herbivore(20, 20, cycle))
world.new_body(bot)

def make_objects():
    for _ in range(20):
        x, y = world.random_coordinates()
        g = Grass(x, y, cycle)
        world.new_body(g)

    # for _ in range(5):
    #     x, y = world.random_coordinates()
    #     p = Predator(x, y, cycle)
    #     world.new_body(p)
