import pygame, sys, random

WIDTH = 800
HEIGHT = 600
SIDEBAR_WIDTH = 200

FPS = 30

CELL_SIZE = 2

CYAN = (0, 128, 255)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

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
            y = random.randint(0, HEIGHT)
            if (x, y) not in Body.all_bodies:
                return x, y

class Player(Body):
    def __init__(self, x, y, birthday, color=BLUE):
        super().__init__(x, y, color, birthday)

    def move_player(self, pressed):
        speed = 1
        if pressed[pygame.K_w]: self.y -= speed
        if pressed[pygame.K_s]: self.y += speed
        if pressed[pygame.K_a]: self.x -= speed
        if pressed[pygame.K_d]: self.x += speed

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
screen = pygame.display.set_mode((WIDTH + SIDEBAR_WIDTH, HEIGHT))  # Создание окна
cycle = 0

player1 = Player(20, 20, cycle)
grass = []

for g in range(20):
    x, y = Body.random_coordinates()
    grass.append(Grass(x, y, cycle))

clock = pygame.time.Clock()

play = True

while play:
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

    pygame.draw.rect(screen, WHITE, (800, 0, 1, HEIGHT))

    # Отображение количества циклов
    font = pygame.font.SysFont("Arial", 18)
    cycle_text = font.render(f"Цикл: {cycle}", True, WHITE)
    screen.blit(cycle_text, (810, 20))

    pygame.display.flip()

    clock.tick(FPS)
