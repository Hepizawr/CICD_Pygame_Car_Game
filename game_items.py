import pygame
import random
import time as tm
from game_config import *


class Background:
    def __init__(self, screen: pygame.surface, bg_path: str = BG_PATH, bg_y: int = 0, min_spead: int = MIN_BG_SPEED, max_speed: int = MAX_BG_SPEED):
        self.screen = screen
        self.y = bg_y
        self.speed = min_spead
        self.max_speed = max_speed
        backgrond_image = pygame.image.load(bg_path)
        self.backgrond_image = pygame.transform.scale(backgrond_image, (DP_HEIGHT, DP_HEIGHT))
        self.backgrond_rect = self.backgrond_image.get_rect(centerx=DP_WIDTH//2, y=self.y)

    def draw(self):
        self.screen.blit(self.backgrond_image, self.backgrond_rect)
        self.screen.blit(self.backgrond_image, (self.backgrond_rect.x, self.backgrond_rect.y - DP_HEIGHT))

    def move(self, time: int, time_to_up: int = TIME_TO_BG_SPEED_UP, delta: int = DELTA_BG_SPEED):
        if self.speed < self.max_speed:
            if time != 0 and time % time_to_up == 0:
                self.speed += delta
        elif self.speed > self.max_speed:
            self.speed = self.max_speed

        if self.backgrond_rect.y + self.speed < DP_HEIGHT:
            self.backgrond_rect.y += self.speed
        else:
            self.backgrond_rect.y = 0


class Car:
    def __init__(self, screen: pygame.surface, car_path: str = CAR_PATH, car_centerx: int = (DP_WIDTH // 2), car_bottom: int = DP_HEIGHT):
        self.screen = screen
        car_image = pygame.image.load(car_path)
        k_car_height = car_image.get_height() / car_image.get_width()
        # self.car_image = pygame.transform.scale(car_image, (DP_WIDTH / 8.5, (DP_WIDTH / 8.5) * k_car_height))
        self.car_image = pygame.transform.scale(car_image, (DP_HEIGHT / 8.5, (DP_HEIGHT / 8.5) * k_car_height))
        self.car_rect = self.car_image.get_rect(centerx=car_centerx, bottom=car_bottom)
        self.headbox = pygame.transform.scale(self.car_image, (self.car_rect.width/1.2, self.car_rect.height/1.2)).get_rect(centerx=self.car_rect.centerx, centery=self.car_rect.centery)
        # self.x = self.car_rect.x
        # self.y = self.car_rect.y

    def draw(self):
        self.screen.blit(self.car_image, self.car_rect)

    def move(self):
        speed = DP_HEIGHT * 0.015
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            if self.car_rect.x > DP_HEIGHT / 5 + DP_DELTA:
                self.car_rect.x -= speed
        elif keys[pygame.K_RIGHT]:
            if self.car_rect.x < DP_HEIGHT - (DP_HEIGHT / 5) - self.car_rect.width + DP_DELTA:
                self.car_rect.x += speed
        elif keys[pygame.K_UP]:
            if self.car_rect.y > 0:
                self.car_rect.y -= speed
        elif keys[pygame.K_DOWN]:
            if self.car_rect.y < DP_HEIGHT - self.car_rect.height:
                self.car_rect.y += speed

        self.headbox.centerx = self.car_rect.centerx
        self.headbox.centery = self.car_rect.centery


class Enemies:
    def __init__(self, screen: pygame.surface):
        self.screen = screen
        self.list = []
        self.car_index_in_list = 0

    def generate(self, time: int):
        if time != 0 and time % TIME_TO_GENERATE_ENEMIE == 0:
            random.seed(tm.time())
            car_model = CARS_PATH[random.randrange(0, len(CARS_PATH))]
            road_line = DP_HEIGHT * (random.randrange(28, 74, 15) / 100) + DP_DELTA
            self.list.append(Car(self.screen, car_model, road_line, -120))

    def draw(self):
        for car in self.list:
            car.draw()

    def __check_object_delete(self):
        for car in self.list:
            if car.car_rect.y > DP_HEIGHT:
                self.list.remove(car)

    def move(self, speed: int):
        for car in self.list:
            car.car_rect.centery += speed
            car.headbox.centery = car.car_rect.centery
        self.__check_object_delete()

    def collision(self, user_car: Car):
        for car in self.list:
            if car.headbox.colliderect(user_car.headbox):
                end_screen(self.screen)


class Coins(Enemies):
    count = 0

    def generate(self, time: int):
        if time != 0 and time % TIME_TO_GENERATE_COIN == 0:
            random.seed(tm.time())
            coin_model = COIN_PATH
            road_line = DP_HEIGHT * (random.randrange(28, 74, 15) / 100) + DP_DELTA
            self.list.append(Car(self.screen, coin_model, road_line, -120))

    def collision(self, user_car: Car):
        for coin in self.list:
            if coin.headbox.colliderect(user_car.headbox):
                self.count += 1
                self.list.remove(coin)


def start_screen(screen: pygame.surface, background: Background):
    running = True

    while running:
        screen.fill(GRAY)
        background.draw()

        button_image = pygame.image.load(BUTTON_PATH)
        k_button_widht = button_image.get_rect().width / button_image.get_rect().height
        button_image = pygame.transform.scale(pygame.image.load(BUTTON_PATH), ((DP_WIDTH//10)*k_button_widht, DP_HEIGHT//10))

        button_start = screen.blit(button_image, button_image.get_rect(centerx=DP_WIDTH // 2, bottom=DP_HEIGHT / 2.5))
        button_exit = screen.blit(button_image, button_image.get_rect(centerx=DP_WIDTH // 2, bottom=DP_HEIGHT / 1.8))

        font_object = pygame.font.Font(pygame.font.get_default_font(), 15)

        button_start_text = font_object.render("Start", True, WHITE)
        bst_rect = button_start_text.get_rect(centerx=button_start.centerx, centery=button_start.centery)
        button_exit_text = font_object.render("Exit", True, WHITE)
        bet_rect = button_exit_text.get_rect(centerx=button_exit.centerx, centery=button_exit.centery)

        screen.blit(button_start_text, bst_rect)
        screen.blit(button_exit_text, bet_rect)

        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_F2:
                    running = False
            elif button_start.collidepoint(pygame.mouse.get_pos()):
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    running = False
            elif button_exit.collidepoint(pygame.mouse.get_pos()):
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    quit()

            if event.type == pygame.QUIT:
                quit()


def pause_screen(screen: pygame.surface):
    running = True

    while running:
        button_image = pygame.image.load(BUTTON_PATH)
        k_button_widht = button_image.get_rect().width / button_image.get_rect().height
        button_image = pygame.transform.scale(pygame.image.load(BUTTON_PATH),
                                              ((DP_WIDTH // 10) * k_button_widht, DP_HEIGHT // 10))

        button_start = screen.blit(button_image, button_image.get_rect(centerx=DP_WIDTH // 2, bottom=DP_HEIGHT / 2.5))
        button_exit = screen.blit(button_image, button_image.get_rect(centerx=DP_WIDTH // 2, bottom=DP_HEIGHT / 1.8))

        font_object = pygame.font.Font(pygame.font.get_default_font(), 15)

        button_start_text = font_object.render("Resume", True, WHITE)
        bst_rect = button_start_text.get_rect(centerx=button_start.centerx, centery=button_start.centery)
        button_exit_text = font_object.render("Exit", True, WHITE)
        bet_rect = button_exit_text.get_rect(centerx=button_exit.centerx, centery=button_exit.centery)

        screen.blit(button_start_text, bst_rect)
        screen.blit(button_exit_text, bet_rect)

        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
            elif button_start.collidepoint(pygame.mouse.get_pos()):
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    running = False
            elif button_exit.collidepoint(pygame.mouse.get_pos()):
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    quit()

            if event.type == pygame.QUIT:
                quit()


def end_screen(screen: pygame.surface):
    running = True

    while running:
        button_image = pygame.image.load(BUTTON_PATH)
        k_button_widht = button_image.get_rect().width / button_image.get_rect().height
        button_image = pygame.transform.scale(pygame.image.load(BUTTON_PATH),
                                              ((DP_WIDTH // 10) * k_button_widht, DP_HEIGHT // 10))

        # button_start = screen.blit(button_image, button_image.get_rect(centerx=DP_WIDTH // 2, bottom=DP_HEIGHT / 2.5))
        button_exit = screen.blit(button_image, button_image.get_rect(centerx=DP_WIDTH // 2, bottom=DP_HEIGHT / 1.8))

        font_object = pygame.font.Font(pygame.font.get_default_font(), 15)

        # button_start_text = font_object.render("Resume", True, WHITE)
        # bst_rect = button_start_text.get_rect(centerx=button_start.centerx, centery=button_start.centery)
        button_exit_text = font_object.render("Exit", True, WHITE)
        bet_rect = button_exit_text.get_rect(centerx=button_exit.centerx, centery=button_exit.centery)

        # screen.blit(button_start_text, bst_rect)
        screen.blit(button_exit_text, bet_rect)

        pygame.display.update()

        for event in pygame.event.get():
            # if event.type == pygame.KEYDOWN:
            #     if event.key == pygame.K_ESCAPE:
            #         running = False
            # elif button_start.collidepoint(pygame.mouse.get_pos()):
            #     if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            #         running = False
            if button_exit.collidepoint(pygame.mouse.get_pos()):
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    quit()

            if event.type == pygame.QUIT:
                quit()


def show_dev_info(show: bool, screen: pygame.surface, time: int, user_car: Car, background: Background, enemies):
    if show:
        font_object = pygame.font.Font(pygame.font.get_default_font(), 15)

        screen.blit(font_object.render(f"Time: {time}", True, BLACK), (10, 10))
        screen.blit(font_object.render(f"Speed: {background.speed}, Max: {background.speed % background.max_speed == 0}", True, BLACK), (10, 30))
        screen.blit(font_object.render(f"User car pos: {[user_car.car_rect.x, user_car.car_rect.y]}", True, BLACK), (10, 50))
        screen.blit(font_object.render(f"Enemies count: {len(enemies.list)}", True, BLACK), (10, 70))
        screen.blit(font_object.render(f"Background Y: {background.backgrond_rect.y}", True, RED), (10, 100))

        for car in enemies.list:
            pygame.draw.rect(screen, BLACK, car.headbox, 1)
            screen.blit(font_object.render(f"{car.car_rect.y}", True, WHITE), (car.car_rect.centerx, car.car_rect.centery))

        pygame.draw.rect(screen, RED, user_car.headbox, 1)


def show_player_info(show: bool, screen: pygame.surface, time: int, coin: Coins, background: Background):
    if not show:
        font_object = pygame.font.Font(pygame.font.get_default_font(), 15)
        screen.blit(font_object.render(f"Time: {int(time)}", True, BLACK), (10, 10))
        screen.blit(font_object.render(f"Coins: {coin.count}", True, BLACK), (10, 30))
        screen.blit(font_object.render(f"Score: {int(int(time) * (background.speed/5))}", True, BLACK), (10, 50))

