import pygame
from game_config import *
from game_items import *

pygame.init()
screen = pygame.display.set_mode((DP_WIDTH, DP_HEIGHT))
clock = pygame.time.Clock()

background = Background(screen)
user_car = Car(screen, CAR_PATH)
enemies = Enemies(screen)
coins = Coins(screen)

frame_count = 0
second_count = 0
bg_y = 0

dev_info = False

start_screen(screen, background)

running = True
while running:
    clock.tick(FPS)

    frame_count += 1
    second_count = frame_count / FPS

    enemies.generate(second_count)
    coins.generate(second_count)

    background.move(second_count)
    coins.move(background.speed)
    enemies.move(background.speed)
    user_car.move()

    screen.fill(GRAY)
    background.draw()
    coins.draw()
    enemies.draw()
    user_car.draw()

    show_dev_info(dev_info, screen, second_count, user_car, background, enemies, coins)
    show_player_info(dev_info, screen, second_count, coins, background)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            quit()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_F1:
                dev_info = not dev_info
            if event.key == pygame.K_ESCAPE:
                pause_screen(screen)

    pygame.display.update()

    enemies.collision(user_car)
    coins.collision(user_car)

