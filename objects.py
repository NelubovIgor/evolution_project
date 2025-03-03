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
        Body.all_bodies[(x, y)] = self

    def update_coordinates(self, new_crd):       
        # print("old coord: ", self.x, self.y)
        Body.clear_body(self)
        Body.all_bodies[new_crd] = self
        # print("new coord: ", self.x, self.y, new_crd)

    def do(self):
        self.energy -= 0.1
        obj = self.touch()
        if not obj:
            self.vision()
        else:
            predators = [o for o in obj if o.__class__.__name__ == "Predator"]
            herbivores = [o for o in obj if o.__class__.__name__ == "Herbivore"]
            grasses = [o for o in obj if o.__class__.__name__ == "Grass"]
            if predators:
                direction = []
                self.move(direction)
            elif herbivores:
                direction = []
                self.move(direction)
            else:
                direction = (grasses[0].x, grasses[0].y)
                self.move(direction)
        return

    def touch(self):
        dir = DIRECTIONS
        def clean_border(direct):
            return {key: value for key, value in dir if direct not in key}
        if self.x == 0: dir = clean_border("n")
        if self.y == 0: dir = clean_border("w")
        if self.x == WIDTH - 1: dir = clean_border("e")
        if self.y == HEIGHT - 1: dir = clean_border("s")
        results = [tuple(a + b for a, b in zip((self.x, self.y), t)) for t in dir.values()]
        objects_touch = [r for r in results if r in Body.all_bodies]
        return objects_touch

    def vision(self):
        pass

    def move(self, direction):
        pass

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
        around = Body.touch(self)
        if around:
            print(around)
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



def grow():
    while not grass_list:
        grass_list.append(Grass(Body.random_coordinates()[0], Body.random_coordinates()[1], cycle))

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


make_objects()

# print(grass_list[0].__class__.__name__)
