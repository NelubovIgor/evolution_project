import pygame, sys, random

WIDTH = 800
HIGHT = 600
FPS = 60

CELL_SIZE = 2

CYAN = (0, 128, 255)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BLACK = (0, 0, 0)

class Body:
    all_bodies = {}

    def __init__(self, x, y, color, birthday):
        self.x = x
        self.y = y
        self.color = color
        self.birthday = birthday
        Body.all_bodies[(x, y)] = self

    def clear_body(self):
        del Body.all_bodies[(self.x, self.y)]

    def random_coordinates():
        while True:
            x = random.randint(0, WIDTH)
            y = random.randint(0, HIGHT)
            if (x, y) not in Body.all_bodies:
                return x, y

class Player(Body):
    def __init__(self, x, y, birthday, color=BLUE):
        super().__init__(x, y, color, birthday)

    def move_player(self, pressed):
        if pressed[pygame.K_w]: player1.y -= 3
        if pressed[pygame.K_s]: player1.y += 3
        if pressed[pygame.K_a]: player1.x -= 3
        if pressed[pygame.K_d]: player1.x += 3

class Grass(Body):
    def __init__(self, x, y, birthday, color=GREEN):
        super().__init__(x, y, color, birthday)

class Predator(Body):
    def __init__(self, x, y, birthday, color=RED):
        super().__init__(x, y, color, birthday)

class Herbivore(Body):
    def __init__(self, x, y, birthday, color=CYAN):
        super().__init__(x, y, color, birthday)

pygame.init()  # Инициализация Pygame
screen = pygame.display.set_mode((WIDTH, HIGHT))  # Создание окна
cycle = 0

player1 = Player(20, 20, cycle)
grass = []

for g in range(20):
    x, y = Body.random_coordinates()
    grass.append(Grass(x, y, cycle))

clock = pygame.time.Clock()

while True:
    cycle += 1
    # Обработка событий
    for e in pygame.event.get():
        if e.type == pygame.QUIT:
            sys.exit()

    pressed = pygame.key.get_pressed()
    if pressed:
        Player.move_player(player1, pressed)

    #отрисовка
    screen.fill(BLACK)

    for g in grass:
        rect = pygame.Rect(g.x, g.y, CELL_SIZE, CELL_SIZE)
        pygame.draw.rect(screen, g.color, rect)

    pygame.draw.rect(screen, player1.color, pygame.Rect(player1.x, player1.y, CELL_SIZE, CELL_SIZE))

    pygame.display.flip()
    clock.tick(FPS)
