import pygame, sys
from constants import *
from objects import *

pygame.init()  # Инициализация Pygame
screen = pygame.display.set_mode((WIDTH + SIDEBAR_WIDTH, HEIGHT))  # Создание окна

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
        for h in herbivore_list:
            Body.do(h)
    else:
        paused = not paused

    if not paused:
        cycle += 1
        # grow()

    #отрисовка
    screen.fill(BLACK)

    for g in grass_list:
        pygame.draw.circle(screen, g.color, (g.x, g.y), g.size)

    for h in herbivore_list:
        pygame.draw.circle(screen, h.color, (h.x, h.y), h.size)

    for p in predator_list:
        pygame.draw.circle(screen, p.color, (p.x, p.y), p.size)

    pygame.draw.circle(screen, player1.color, (player1.x, player1.y), player1.size)
    

    pygame.draw.rect(screen, WHITE, (800, 0, 1, HEIGHT))

    # Отображение количества циклов
    font = pygame.font.SysFont("Arial", 18)
    cycle_text = font.render(f"Цикл: {cycle}", True, WHITE)
    screen.blit(cycle_text, (810, 20))

    #координаты игрока
    coordinates = font.render(f"Player: х {player1.x},у {player1.y}", True, WHITE)
    screen.blit(coordinates, (810, 40))

    coordinates_b = font.render(f"Bot: х {herbivore_list[0].x},у {herbivore_list[0].y}", True, WHITE)
    screen.blit(coordinates_b, (810, 60))

    pygame.display.flip()

    clock.tick(FPS)
