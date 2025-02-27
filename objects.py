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

    def touch(self):
        pass

    def vision(self):
        pass

    def move(self):
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
        # res = []
        for obj in Body.all_bodies.keys():
            # print(obj, self, sep='\n')
            if obj != (self.x, self.y):
                distance = math.hypot(self.x - obj[0], self.y - obj[1])
                if distance < (self.size + Body.all_bodies[obj].size):
                    # print(Body.all_bodies[obj])
                    grass_list.remove(Body.all_bodies[obj])
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

grass_list.append(Grass(40, 40, cycle))

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


# make_objects()
