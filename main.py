import pygame, sys
from constants import *
from objects import *

pygame.init()  # Инициализация Pygame
screen = pygame.display.set_mode((WIDTH + SIDEBAR_WIDTH, HEIGHT))  # Создание окна

clock = pygame.time.Clock()

paused = True
player1_on = False
player1 = None
tests_obj()

while True:
    # Обработка событий
    for e in pygame.event.get():
        if e.type == pygame.QUIT:
            sys.exit()

    pressed = pygame.key.get_pressed()

    if pressed[pygame.K_SPACE]:
        paused = not paused


    if not paused:
        # print("1")
        if player1_on:
            if not player1:
                player1 = make_player()
            Player.move_player(player1, pressed)
        cycle += 1
        # make_objects()
        grow()
        for h in herbivore_list:
            # print("do")
            Body.do(h)




    #отрисовка
    screen.fill(BLACK)

    for g in grass_list:
        pygame.draw.circle(screen, g.color, (g.x, g.y), g.size)

    for h in herbivore_list:
        pygame.draw.circle(screen, h.color, (h.x, h.y), h.size)

    for p in predator_list:
        pygame.draw.circle(screen, p.color, (p.x, p.y), p.size)

    if player1_on:
        pygame.draw.circle(screen, player1.color, (player1.x, player1.y), player1.size)
    

    pygame.draw.rect(screen, WHITE, (WIDTH, 0, 1, HEIGHT))

    # Отображение количества циклов
    font = pygame.font.SysFont("Arial", 18)
    cycle_text = font.render(f"Цикл: {cycle}", True, WHITE)
    screen.blit(cycle_text, (WIDTH + 10, 20))

    #координаты игрока
    if player1_on:
        coordinates = font.render(f"Player: х {player1.x},у {player1.y}", True, WHITE)
        screen.blit(coordinates, (WIDTH + 10, 40))


    coordinates_b = font.render(f"Bot: х {herbivore_list[0].x},у {herbivore_list[0].y}", True, WHITE)
    screen.blit(coordinates_b, (WIDTH + 10, 60))

    energy_b = font.render(f"Bot energy: {herbivore_list[0].energy}", True, WHITE)
    screen.blit(energy_b, (WIDTH + 10, 80))

    pygame.display.flip()

    clock.tick(FPS)
