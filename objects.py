import random, pygame, math, logging
from constants import *
import copy

# Настройка логирования
logging.basicConfig(
    filename="simulation.log", level=logging.DEBUG,
    format="%(asctime)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

class World:
    def __init__(self):
        self.bodies = {}
        self.id_to_coords = {}
        self.next_id = 0
        self.cycle = 0
        logger.info("the world is initialized")

    def world_life(self):
        self.cycle += 1
        logger.debug(f"the start of cycle {self.cycle}")
        copy_world = copy.copy(self.bodies)
        for obj in copy_world.values():
            if isinstance(obj, Animal):
                obj.do()
            elif isinstance(obj, Grass):
                obj.grow()
            
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
            
    def borders(obj, visible):
        min_x = max(0, obj.x - visible)
        max_x = min(WIDTH, obj.x + visible + 1)
        min_y = max(0, obj.y - visible)
        max_y = min(HEIGHT, obj.y + visible + 1)
        return min_x, max_x, min_y, max_y

    def clear_body(self, obj):
        id = obj.id
        del self.bodies[(obj.x, obj.y)]
        del self.id_to_coords[id]

    def update_coordinates(self, obj, old_obj):
        if (obj.x, obj.y) in self.bodies: 
            self.clear_body(old_obj)
        self.add_body(obj)

    def collision(self, obj, target):
        distance = math.hypot((target.x - obj.x) ** 2 + (target.y - obj.y) ** 2)
        radius_sum = obj.size + target.size

        if distance <= radius_sum:
            energy = target.energy
            self.clear_body(target)
            # print(energy)
            return energy
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
        self.memory = ()
        self.genome = []
        self.speed = speed
        self.id = None

    def vision(self, visible=1):
        objects_around = []

        min_x, max_x, min_y, max_y = World.borders(self, visible)

        for x in range(min_x, max_x):
            for y in range(min_y, max_y):
                if x == self.x and y == self.y:
                    continue
                if (x, y) in world.bodies:
                    objects_around.append(world.bodies[(x, y)])
        return objects_around
    
    def reproduction(self, place):
        self.energy /= 2
        if isinstance(self, Herbivore):
            world.new_body(Herbivore(place[0], place[1], world.cycle, energy=self.energy))
        elif isinstance(self, Grass):
            world.new_body(Grass(place[0], place[1], world.cycle, energy=self.energy))

    def sleep(self):
        pass

class Animal(Body):
    def __init__(self, x, y, birthday, color, energy):
        super().__init__(x, y, birthday, color, energy)

    def do(self):
        if self.energy <= 0:
            world.clear_body(self)
        elif self.energy > 200:
            min_x, max_x, min_y, max_y = World.borders(self, 1)
            x = random.randint(min_x, max_x)
            y = random.randint(min_y, max_y)
            if (x, y) not in world.bodies:
                self.reproduction((x, y))
        else:
            for _ in range(self.speed):
                self.energy -= 0.1
                copy_obj = copy.copy(self)
                obj = self.vision()
                if not obj:
                    obj = self.vision(self.visible)
                if not obj:
                    if not self.memory:
                        logger.info("start memory")
                        min_x, max_x, min_y, max_y = World.borders(self, self.visible)
                        x = random.randint(min_x, max_x)
                        y = random.randint(min_y, max_y)
                        self.memory = (x, y)
                        self.move(self.memory)
                        world.update_coordinates(self, copy_obj)
                    elif self.memory == (self.x, self.y):
                        logger.info("clear memory")
                        self.memory = ()
                    elif self.memory:
                        logger.info("move memory")
                        self.move(self.memory)
                        world.update_coordinates(self, copy_obj)

                if obj:
                    self.memory = ()
                    logger.info("see target")
                    target = random.choice(obj)
                    self.move((target.x, target.y))
                    eat = world.collision(self, target)
                    if eat:
                        self.energy += eat
                    world.update_coordinates(self, copy_obj)
        
    def move(self, target, to_target=True):
        dir_x = target[0] - self.x
        dir_y = target[1] - self.y

        if dir_x != 0:
            to_x = int(dir_x / dir_x) if dir_x > 0 else int((dir_x / dir_x) * -1)
        else:
            to_x = 0

        if dir_y != 0:
            to_y = int(dir_y / dir_y) if dir_y > 0 else int((dir_y / dir_y) * -1)
        else:
            to_y = 0

        if to_target:
            self.x += to_x
            self.y += to_y
        else:
            self.x -= to_x
            self.y -= to_y

class Grass(Body):
    def __init__(self, x, y, birthday, color=GREEN, energy=100):
        super().__init__(x, y, birthday, color, energy)

    def grow(self):
        self.energy += 1

        if self.energy >= 100:
            min_x, max_x, min_y, max_y = World.borders(self, self.visible)
            count_step = 0
            while count_step < 3:
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
    def __init__(self, x, y, birthday, color=CYAN, energy=100):
        super().__init__(x, y, birthday, color, energy)

class Player(Body):
    def __init__(self, x, y, birthday, color=BLUE):
        super().__init__(x, y, birthday, color)

    def move_player(self, pressed):
        copy_obj = copy.copy(self)
        speed = 1
        new_x, new_y = self.x, self.y
        if pressed[pygame.K_w]:
            self.y -= speed
        if pressed[pygame.K_s]:
            self.y += speed
        if pressed[pygame.K_a]:
            self.x -= speed
        if pressed[pygame.K_d]:
            self.x += speed

        if (new_x, new_y) != (self.x, self.y):  # Проверка, изменились ли координаты
            self.x, self.y = new_x, new_y
            world.update_coordinates(self, copy_obj)



world = World()
play = False

# создание объектов
if play:
    player1 = Player(200, 200, world.cycle)
    world.new_body(player1)
else:
    player1 = None

food = (Grass(30, 21, world.cycle))
world.new_body(food)

food1 = (Grass(61, 20, world.cycle))
world.new_body(food1)

# food2 = (Grass(21, 21, cycle))
# world.new_body(food2)

# food = (Grass(34, 20, cycle))
# world.new_body(food)

# food3 = (Grass(44, 20, cycle))
# world.new_body(food3)

# food4 = (Grass(54, 20, cycle))
# world.new_body(food4)

# bot = (Herbivore(20, 20, cycle))
# world.new_body(bot)

bot = (Herbivore(20, 20, world.cycle))
world.new_body(bot)

def make_objects():
    for _ in range(20):
        x, y = world.random_coordinates()
        g = Grass(x, y, world.cycle)
        world.new_body(g)

    # for _ in range(5):
    #     x, y = world.random_coordinates()
    #     p = Predator(x, y, cycle)
    #     world.new_body(p)
