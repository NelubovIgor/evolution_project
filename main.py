import pygame, sys
from constants import *
from objects import *

pygame.init()  # Инициализация Pygame
screen = pygame.display.set_mode((WIDTH + SIDEBAR_WIDTH, HEIGHT))  # Создание окна

clock = pygame.time.Clock()

paused = True


make_objects()

while True:
    # Обработка событий
    for e in pygame.event.get():
        if e.type == pygame.QUIT:
            sys.exit()

    pressed = pygame.key.get_pressed()

    if pressed[pygame.K_SPACE]:
        paused = not paused

    if not paused:
        if player1:
            Player.move_player(player1, pressed)
        world.world_life()

    #отрисовка
    screen.fill(BLACK)

    for c, b in world.bodies.items():
        pygame.draw.circle(screen, b.color, (c[0], c[1]), b.size)

    if player1:
        pygame.draw.circle(screen, player1.color, (player1.x, player1.y), player1.size)
    
    pygame.draw.rect(screen, WHITE, (800, 0, 1, HEIGHT))

    # Отображение количества циклов
    font = pygame.font.SysFont("Arial", 18)
    cycle_text = font.render(f"Cycle: {world.cycle}", True, WHITE)
    screen.blit(cycle_text, (810, 20))
    len_bot = font.render(f"the number of bots: {len(world.bodies)}", True, WHITE)
    screen.blit(len_bot, (810, 120))

    # координаты игрока
    if player1:
        coordinates = font.render(f"Player: х {player1.x},у {player1.y}", True, WHITE)
        screen.blit(coordinates, (810, 40))

    # координаты еды
    if food1:
        coordinates_b = font.render(f"Food: х {food1.x},у {food1.y}", True, WHITE)
    else:
        coordinates_b = font.render(f"None", True, WHITE)

    screen.blit(coordinates_b, (810, 100))

    if bot:
        coordinates_c = font.render(f"Bot: х {bot.x},у {bot.y}", True, WHITE)
        screen.blit(coordinates_c, (810, 60))

        energy_b = font.render(f"Bot energy: {bot.energy}", True, WHITE)
        screen.blit(energy_b, (810, 80))

    pygame.display.flip()

    clock.tick(FPS)
