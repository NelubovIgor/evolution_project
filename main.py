import pygame, sys, random

WIDTH = 800
HEIGHT = 600
SIDEBAR_WIDTH = 200

FPS = 30

CELL_SIZE = 1

CYAN = (0, 128, 255)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

class Body:
    all_bodies = {}

    def __init__(self, x, y, color, birthday, energy=100, size=CELL_SIZE):
        self.x = x
        self.y = y
        self.color = color
        self.birthday = birthday
        self.energy = energy
        self.size = size
        Body.all_bodies[(x, y)] = self

    def update_coordinates(self, new_crd):
        Body.clear_body(self)
        Body.all_bodies[new_crd] = self

    def clear_body(self):
        del Body.all_bodies[(self.x, self.y)]

    def random_coordinates():
        while True:
            x = random.randint(0, WIDTH)
            y = random.randint(0, HEIGHT)
            if (x, y) not in Body.all_bodies:
                return x, y
            
    def collision(self):
        pass

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

class Grass(Body):
    def __init__(self, x, y, birthday, color=GREEN, size=CELL_SIZE):
        super().__init__(x, y, color, birthday, size)

class Predator(Body):
    def __init__(self, x, y, birthday, color=RED):
        super().__init__(x, y, color, birthday)

class Herbivore(Body):
    def __init__(self, x, y, birthday, color=CYAN):
        super().__init__(x, y, color, birthday)

pygame.init()  # Инициализация Pygame
screen = pygame.display.set_mode((WIDTH + SIDEBAR_WIDTH, HEIGHT))  # Создание окна

cycle = 0

# создание объектов
player1 = Player(20, 20, cycle)
grass_list = []
herbivore_list = []
predator_list = []

for g in range(20):
    x, y = Body.random_coordinates()
    grass_list.append(Grass(x, y, cycle))

for h in range(5):
    x, y = Body.random_coordinates()
    herbivore_list.append(Herbivore(x, y, cycle))

for p in range(5):
    x, y = Body.random_coordinates()
    predator_list.append(Predator(x, y, cycle))

clock = pygame.time.Clock()

paused = False

while True:
    # Обработка событий
    for e in pygame.event.get():
        if e.type == pygame.QUIT:
            sys.exit()

    pressed = pygame.key.get_pressed()
    if not pressed[pygame.K_SPACE]:
        Player.move_player(player1, pressed)
    else:
        paused = not paused

    if not paused:
        cycle += 1

    #отрисовка
    screen.fill(BLACK)

    for g in grass_list:
        rect = pygame.Rect(g.x, g.y, g.size, g.size)
        pygame.draw.rect(screen, g.color, rect)

    for h in herbivore_list:
        rect = pygame.Rect(h.x, h.y, h.size, h.size)
        pygame.draw.rect(screen, h.color, rect)

    for p in predator_list:
        rect = pygame.Rect(p.x, p.y, p.size, p.size)
        pygame.draw.rect(screen, p.color, rect)

    pygame.draw.rect(screen, player1.color, pygame.Rect(player1.x, player1.y, player1.size, player1.size))

    pygame.draw.rect(screen, WHITE, (800, 0, 1, HEIGHT))

    # Отображение количества циклов
    font = pygame.font.SysFont("Arial", 18)
    cycle_text = font.render(f"Цикл: {cycle}", True, WHITE)
    screen.blit(cycle_text, (810, 20))

    #координаты игрока
    coordinates = font.render(f"Координаты: х {player1.x},у {player1.y}", True, WHITE)
    screen.blit(coordinates, (810, 40))

    pygame.display.flip()

    clock.tick(FPS)
