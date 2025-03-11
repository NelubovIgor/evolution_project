import random, pygame, math
from constants import *


class Body:
    all_bodies = {}

    def __init__(self, x, y, color, birthday, energy=100, size=CELL_SIZE, visible=3):
        self.x = x
        self.y = y
        self.color = color
        self.birthday = birthday
        self.energy = energy
        self.size = size
        self.visible = visible
        self.memory = []
        
        Body.all_bodies[(x, y)] = self

    def update_coordinates(self, new_crd):       
        # print("old coord: ", self.x, self.y)
        Body.clear_body(self)
        Body.all_bodies[new_crd] = self
        # print("new coord: ", self.x, self.y, new_crd)

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

        if not obj and not self.memory:
            direction = tuple(a + b for a, b in zip(random.choice(list(DIRECTIONS.values())), (self.x, self.y)))
            self.move(direction)
            return
        elif self.memory:
            if len(self.memory) == 1:
                self.memory.append(10)
            self.memory[1] -= 1
            self.move(None)
            if self.memory[1] == 0:
                self.memory.clear()
            return

        predators = [o for o in obj if o.__class__.__name__ == "Predator"]
        herbivores = [o for o in obj if o.__class__.__name__ == "Herbivore"]
        grasses = [o for o in obj if o.__class__.__name__ == "Grass"]
        if predators:
            pred = random.choice(predators)
            self.move((pred.x, pred.y), False)
        elif herbivores:
            herb = random.choice(herbivores)
            self.move((herb.x, herb.y), False)
        elif grasses:
            gras = random.choice(herbivores)
            self.move((gras.x, gras.y))
        else:
            self.sleep()
            return
        
    def sleep(self):
        pass

    # def borders(self):
    #     dir = DIRECTIONS
    #     def clean_border(direct):
    #         return {key: value for key, value in dir if direct not in key}
    #     if self.x == 0: dir = clean_border("n")
    #     if self.y == 0: dir = clean_border("w")
    #     if self.x == WIDTH - 1: dir = clean_border("e")
    #     if self.y == HEIGHT - 1: dir = clean_border("s")

    # def touch(self):
    #     direction = self.borders()
    #     results = [tuple(a + b for a, b in zip((self.x, self.y), t)) for t in direction.values()]
    #     objects_touch = [r for r in results if r in Body.all_bodies]
    #     return objects_touch

    def vision(self, visible=1):
        objects = []

        x_min = int(self.x - visible)
        x_max = int(self.x + visible) 
        y_min = int(self.y - visible)
        y_max = int(self.y + visible)

        # Проходим по всем точкам в области
        for x in range(x_min, x_max):
            for y in range(y_min, y_max):
                if (self.x == x and self.y == y) and 0 < x < WIDTH or 0 < y < HEIGHT:
                    print("pass")
                    pass
                if (x - self.x) ** 2 + (y - self.y) ** 2 <= visible ** 2:
                    if (x, y) in Body.all_bodies:
                        objects.append(Body.all_bodies[(x, y)])
        return objects


    def move(self, target, to_target=True):
        if not target:
            self.x += self.memory[0][0]
            self.y += self.memory[0][1]
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
        if 0 <= self.x <= WIDTH or 0 <= self.y <= HEIGHT:
            self.memory.clear()
        self.collision()

    def clear_body(self):
        if (self.x, self.y) in Body.all_bodies:
            # print(Body.all_bodies)
            del Body.all_bodies[(self.x, self.y)]

    def random_coordinates():
        while True:
            x = random.randint(0, WIDTH)
            y = random.randint(0, HEIGHT)
            if (x, y) not in Body.all_bodies:
                return x, y

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
                            herbivore_list.remove(body_obj)
                        elif name == "Predator":
                            predator_list.remove(body_obj)
                        Body.clear_body(Body.all_bodies[obj])
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
player1 = Player(20, 20, cycle)

grass_list = []
herbivore_list = []
predator_list = []

# grass_list.append(Grass(12, 12, cycle))

herbivore_list.append(Herbivore(12, 12, cycle))

# def grow():
#     while not grass_list:
#         grass_list.append(Grass(Body.random_coordinates()[0], Body.random_coordinates()[1], cycle))

def make_objects():
    for g in range(20):
        x, y = Body.random_coordinates()
        grass_list.append(Grass(x, y, cycle))

    # for h in range(5):
    #     x, y = Body.random_coordinates()
    #     herbivore_list.append(Herbivore(x, y, cycle))

    for p in range(5):
        x, y = Body.random_coordinates()
        predator_list.append(Predator(x, y, cycle))


make_objects()

# print(Body.all_bodies[(12, 12)])

# print(grass_list[0].__class__.__name__)
