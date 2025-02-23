import random, pygame, math
from constatnts import *


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
        Body.clear_body(self)
        Body.all_bodies[new_crd] = self

    def touch(self):
        pass

    def vision(self):
        pass

    def move(self):
        pass

    def clear_body(self):
        if (self.x, self.y) in Body.all_bodies:
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
            distance = math.hypot(self.x - obj[0], self.y - obj[1])
            if distance < (self.size + Body.all_bodies[obj].size):
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
            Body.update_coordinates(self, (self.x, self.y - speed))
            self.y -= speed
        if pressed[pygame.K_s]:
            Body.update_coordinates(self, (self.x, self.y + speed))
            self.y += speed
        if pressed[pygame.K_a]:
            Body.update_coordinates(self, (self.x - speed, self.y))
            self.x -= speed
        if pressed[pygame.K_d]:
            Body.update_coordinates(self, (self.x + speed, self.y))
            self.x += speed
        Body.collision(self)
