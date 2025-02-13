import pygame
import random
import math

# Настройки окна
WIDTH, HEIGHT = 800, 600
FPS = 30

# Цвета
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BROWN = (139, 69, 19)

# Инициализация Pygame
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()

class Plant:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.energy = 10
        self.reproduction_time = random.randint(50, 100)

    def update(self):
        self.reproduction_time -= 1
        if self.reproduction_time <= 0:
            self.reproduce()
            self.reproduction_time = random.randint(50, 100)

    def reproduce(self):
        # Создание нового растения в случайном радиусе
        new_x = self.x + random.randint(-50, 50)
        new_y = self.y + random.randint(-50, 50)
        if 0 <= new_x < WIDTH and 0 <= new_y < HEIGHT:
            plants.append(Plant(new_x, new_y))

    def draw(self):
        pygame.draw.circle(screen, GREEN, (self.x, self.y), 5)

class Herbivore:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.energy = 50
        self.speed = 2
        self.reproduction_energy = 100

    def update(self):
        self.energy -= 0.1
        if self.energy <= 0:
            herbivores.remove(self)
            return

        # Поиск ближайшего растения
        nearest_plant = None
        min_distance = float('inf')
        for plant in plants:
            distance = math.hypot(self.x - plant.x, self.y - plant.y)
            if distance < min_distance:
                min_distance = distance
                nearest_plant = plant

        # Движение к растению
        if nearest_plant:
            angle = math.atan2(nearest_plant.y - self.y, nearest_plant.x - self.x)
            self.x += self.speed * math.cos(angle)
            self.y += self.speed * math.sin(angle)

            # Поедание растения
            if min_distance < 10:
                self.energy += 20
                plants.remove(nearest_plant)

        # Размножение
        if self.energy >= self.reproduction_energy:
            self.energy /= 2
            herbivores.append(Herbivore(self.x + random.randint(-20, 20), self.y + random.randint(-20, 20)))

        # Избегание хищников
        for predator in predators:
            distance = math.hypot(self.x - predator.x, self.y - predator.y)
            if distance < 50:  # Если хищник близко, убегаем
                angle = math.atan2(self.y - predator.y, self.x - predator.x)
                self.x += self.speed * math.cos(angle)
                self.y += self.speed * math.sin(angle)

    def draw(self):
        pygame.draw.circle(screen, BROWN, (self.x, self.y), 8)

class Predator:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.energy = 50
        self.speed = 3
        self.reproduction_energy = 100

    def update(self):
        self.energy -= 0.2
        if self.energy <= 0:
            predators.remove(self)
            return

        # Поиск ближайшего травоядного
        nearest_herbivore = None
        min_distance = float('inf')
        for herbivore in herbivores:
            distance = math.hypot(self.x - herbivore.x, self.y - herbivore.y)
            if distance < min_distance:
                min_distance = distance
                nearest_herbivore = herbivore

        # Движение к травоядному
        if nearest_herbivore:
            angle = math.atan2(nearest_herbivore.y - self.y, nearest_herbivore.x - self.x)
            self.x += self.speed * math.cos(angle)
            self.y += self.speed * math.sin(angle)

            # Поедание травоядного
            if min_distance < 10:
                self.energy += 30
                herbivores.remove(nearest_herbivore)

        # Размножение
        if self.energy >= self.reproduction_energy:
            self.energy /= 2
            predators.append(Predator(self.x + random.randint(-20, 20), self.y + random.randint(-20, 20)))

    def draw(self):
        pygame.draw.circle(screen, RED, (self.x, self.y), 10)


# Создание начальной популяции
plants = [Plant(random.randint(0, WIDTH), random.randint(0, HEIGHT)) for _ in range(20)]
herbivores = [Herbivore(random.randint(0, WIDTH), random.randint(0, HEIGHT)) for _ in range(10)]
predators = [Predator(random.randint(0, WIDTH), random.randint(0, HEIGHT)) for _ in range(5)]

# Основной цикл
running = True
while running:
    screen.fill(WHITE)

    # Обработка событий
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Обновление и отрисовка
    for plant in plants:
        plant.update()
        plant.draw()

    for herbivore in herbivores:
        herbivore.update()
        herbivore.draw()

    for predator in predators:
        predator.update()
        predator.draw()

    pygame.display.flip()
    clock.tick(FPS)

pygame.quit()
