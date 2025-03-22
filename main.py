import pygame, sys
from constants import *
from objects import *

pygame.init()  # Инициализация Pygame
screen = pygame.display.set_mode((WIDTH + SIDEBAR_WIDTH, HEIGHT))  # Создание окна

clock = pygame.time.Clock()

paused = False

# make_objects()

while True:
    # Обработка событий
    for e in pygame.event.get():
        if e.type == pygame.QUIT:
            sys.exit()

    pressed = pygame.key.get_pressed()

    if pressed[pygame.K_SPACE]:
        paused = not paused

    if not paused:
        Player.move_player(player1, pressed)
        cycle += 1

        world.world_life()


        # grow()

    #отрисовка
    screen.fill(BLACK)

    for c, b in world.bodies.items():
        pygame.draw.circle(screen, b.color, (c[0], c[1]), b.size)

    pygame.draw.circle(screen, player1.color, (player1.x, player1.y), player1.size)
    

    pygame.draw.rect(screen, WHITE, (800, 0, 1, HEIGHT))

    # Отображение количества циклов
    font = pygame.font.SysFont("Arial", 18)
    cycle_text = font.render(f"Цикл: {cycle}", True, WHITE)
    screen.blit(cycle_text, (810, 20))

    #координаты игрока
    coordinates = font.render(f"Player: х {player1.x},у {player1.y}", True, WHITE)
    screen.blit(coordinates, (810, 40))



    coordinates_b = font.render(f"Bot: х {bot.x},у {bot.y}", True, WHITE)
    screen.blit(coordinates_b, (810, 60))

    energy_b = font.render(f"Bot energy: {bot.energy}", True, WHITE)
    screen.blit(energy_b, (810, 80))

    pygame.display.flip()

    clock.tick(FPS)
