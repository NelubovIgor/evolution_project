import random, pygame, math
from constants import *


class Body:
    all_bodies = {}

    def __init__(self, x, y, color, birthday, energy=100, size=CELL_SIZE, visible=5, mempoint=5):
        self.x = x
        self.y = y
        self.color = color
        self.birthday = birthday
        self.energy = energy
        self.size = size
        self.visible = visible
        self.memory = []
        self.mempoint = mempoint
        
        Body.all_bodies[(x, y)] = self



    def do(self):
        self.energy -= 0.1
        # obj = self.touch()
        touch = self.vision()

        if not touch:
            obj = self.vision(self.visible)
        else:
            obj = touch
        # print("touch: ", touch)
        # print("obj: ", obj)
        # print("1", self.memory)
        if not obj and not self.memory:
            direction = tuple(a + b for a, b in zip(random.choice(list(DIRECTIONS.values())), (self.x, self.y)))
            self.move(direction)
            return
        elif self.memory:
            # print("memory")
            if len(self.memory) == 1:
                self.memory.append(self.mempoint)
            self.memory[1] -= 1
            self.move(None)
            if self.memory[1] == 0:
                self.memory.clear()
            return
        # print("2", self.memory)
        predators = [o for o in obj if o.__class__.__name__ == "Predator"]
        herbivores = [o for o in obj if o.__class__.__name__ == "Herbivore"]
        grasses = [o for o in obj if o.__class__.__name__ == "Grass"]
        # print(grasses)
        if predators:
            pred = random.choice(predators)
            self.move((pred.x, pred.y), False)
        elif herbivores:
            herb = random.choice(herbivores)
            self.move((herb.x, herb.y), False)
        elif grasses:
            print("see grass")
            gras = random.choice(grasses)
            self.move((gras.x, gras.y))
        else:
            self.sleep()
            return
        

    def vision(self, visible=1):
        objects = []

        x_min = int(self.x - visible)
        x_max = int(self.x + visible) 
        y_min = int(self.y - visible)
        y_max = int(self.y + visible)

        for x in range(x_min, x_max):
            for y in range(y_min, y_max):
                if (0 > x > WIDTH) or (0 > y > HEIGHT):
                    continue
                if self.x == x and self.y == y:
                    # print("self")
                    continue
                if (x - self.x) ** 2 + (y - self.y) ** 2 <= visible ** 2:
                    if (x, y) in Body.all_bodies:
                        # print(x, y)
                        objects.append(Body.all_bodies[(x, y)])
        return objects


    def move(self, target, to_target=True):
        if not target:
            new_x = self.x + self.memory[0][0]
            new_y = self.y + self.memory[0][1]
            self.x = new_x
            self.y = new_y
            self.update_coordinates((new_x, new_y))
            self.collision()
            return
        dx = target[0] - self.x
        dy = target[1] - self.y


        direction_x = 0 if dx == 0 else dx // abs(dx)
        direction_y = 0 if dy == 0 else dy // abs(dy)

        self.memory.append((direction_x, direction_y))

        if to_target:
            self.x += direction_x
            self.y += direction_y
        else:
            self.x -= direction_x
            self.y -= direction_y
        if 0 >= self.x > WIDTH or 0 >= self.y > HEIGHT:
            self.memory.clear()
        self.update_coordinates(target)
        self.collision()


    def sleep(self):
        return

    def clear_body(self):
        if (self.x, self.y) in Body.all_bodies:
            # print(Body.all_bodies)
            del Body.all_bodies[(self.x, self.y)]

    def update_coordinates(self, new_crd):       
        # print("old coord: ", self.x, self.y)
        Body.clear_body(self)
        Body.all_bodies[new_crd] = self
        # print("new coord: ", self.x, self.y, new_crd)

    def collision(self):
        around = self.vision()
        if around:
            # print(around)
            for obj in Body.all_bodies.keys():
                # print(obj, self, sep='\n')
                if obj != (self.x, self.y):
                    distance = math.hypot(self.x - obj[0], self.y - obj[1])
                    if distance < (self.size + Body.all_bodies[obj].size):
                        # print(Body.all_bodies[obj].__class__.__name__)
                        body_obj = Body.all_bodies[obj]
                        name = body_obj.__class__.__name__ 
                        if name == "Grass":
                            grass_list.remove(body_obj)
                        elif name == "Herbivore":
                            print("herbivore dead")
                            herbivore_list.remove(body_obj)
                        elif name == "Predator":
                            predator_list.remove(body_obj)
                        Body.clear_body(Body.all_bodies[obj])
                        break

    @staticmethod
    def random_coordinates():
        while True:
            x = random.randint(0, WIDTH)
            y = random.randint(0, HEIGHT)
            if (x, y) not in Body.all_bodies:
                return x, y

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
            self.y -= speed
        if pressed[pygame.K_s]:
            self.update_coordinates((self.x, self.y + speed))
            self.y += speed
        if pressed[pygame.K_a]:
            self.update_coordinates((self.x - speed, self.y))
            self.x -= speed
        if pressed[pygame.K_d]:
            self.update_coordinates((self.x + speed, self.y))
            self.x += speed    
        self.collision()

cycle = 0


# создание объектов


grass_list = []
herbivore_list = []
predator_list = []
# player1 = None

# grass_list.append(Grass(15, 15, cycle))
def tests_obj():
    grass_list.append(Grass(10, 15, cycle))
    grass_list.append(Grass(10, 13, cycle))
    herbivore_list.append(Herbivore(10, 10, cycle))
    herbivore_list.append(Herbivore(100, 100, cycle))

def grow():
    while not grass_list:
        grass_list.append(Grass(Body.random_coordinates()[0], Body.random_coordinates()[1], cycle))

def make_player():

    return Player(20, 20, cycle)

def make_objects():
    for g in range(20):
        x, y = Body.random_coordinates()
        grass_list.append(Grass(x, y, cycle))

    for h in range(5):
        x, y = Body.random_coordinates()
        herbivore_list.append(Herbivore(x, y, cycle))

    for p in range(5):
        x, y = Body.random_coordinates()
        predator_list.append(Predator(x, y, cycle))




# print(Body.all_bodies[(12, 12)])

# print(grass_list[0].__class__.__name__)
