import pygame
import random
import argparse
from abc import ABC, abstractmethod
import time as tm
from game_config import *


class Background:
    def __init__(self, screen: pygame.surface, bg_path: str = BG_PATH, bg_y: int = 0, min_spead: int = MIN_BG_SPEED,
                 max_speed: int = MAX_BG_SPEED):
        self.screen = screen
        self.y = bg_y
        self.speed = min_spead
        self.max_speed = max_speed
        image = pygame.image.load(bg_path)
        self.image = pygame.transform.scale(image, (DP_HEIGHT, DP_HEIGHT))
        self.rect = self.image.get_rect(centerx=DP_WIDTH // 2, y=self.y)

    def draw(self):
        self.screen.blit(self.image, self.rect)
        self.screen.blit(self.image, (self.rect.x, self.rect.y - DP_HEIGHT))

    def move(self, time: int, time_to_up: int = TIME_TO_BG_SPEED_UP, delta: int = DELTA_BG_SPEED):
        if self.speed < self.max_speed:
            if time != 0 and time % time_to_up == 0:
                self.speed += delta
        elif self.speed > self.max_speed:
            self.speed = self.max_speed

        if self.rect.y + self.speed < DP_HEIGHT:
            self.rect.y += self.speed
        else:
            self.rect.y = 0


def get_car_right_image(model_path: str):
    image = pygame.image.load(model_path)
    k_height = image.get_height() / image.get_width()
    return pygame.transform.scale(image, (DP_HEIGHT / 8.5, (DP_HEIGHT / 8.5) * k_height))


class RoadObject:
    def __init__(self, screen: pygame.surface, model_path: str, ob_centerx: int = (DP_WIDTH // 2),
                 ob_bottom: int = DP_HEIGHT, ob_rotate: bool = False):
        self.screen = screen
        self.ob_rotate = ob_rotate
        image = get_car_right_image(model_path)
        self.image = pygame.transform.rotate(image, 180 * self.ob_rotate)
        self.rect = self.image.get_rect(centerx=ob_centerx, bottom=ob_bottom)
        self.hitbox = pygame.transform.scale(self.image,
                                             (self.rect.width * K_HITBOX, self.rect.height * K_HITBOX)).get_rect(
            centerx=self.rect.centerx, centery=self.rect.centery)

    def draw(self):
        self.screen.blit(self.image, self.rect)


class Car(RoadObject):
    health = USER_CAR_HEALTH
    damage_taken = False
    invulnerable_time_start = 0

    def move(self):
        speed = DP_HEIGHT * 0.015
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            if self.rect.x > DP_HEIGHT / 5 + DP_DELTA:
                self.rect.x -= speed
        elif keys[pygame.K_RIGHT]:
            if self.rect.x < DP_HEIGHT - (DP_HEIGHT / 5) - self.rect.width + DP_DELTA:
                self.rect.x += speed
        elif keys[pygame.K_UP]:
            if self.rect.y > 0:
                self.rect.y -= speed
        elif keys[pygame.K_DOWN]:
            if self.rect.y < DP_HEIGHT - self.rect.height:
                self.rect.y += speed

        self.hitbox.centerx = self.rect.centerx
        self.hitbox.centery = self.rect.centery

    def make_invulnerable(self, time: int, frame: int):
        if self.damage_taken and self.health > 0:
            if int(time - self.invulnerable_time_start) != USER_CAR_INVULNERABLE_TIME:
                self.image = get_car_right_image(CAR_SPIRIT_PATH) if frame % 6 in (0, 1, 2) else get_car_right_image(CAR_PATH)
            else:
                self.image = get_car_right_image(CAR_PATH)
                self.damage_taken = False


class RoadObjects(ABC):
    def __init__(self, screen: pygame.surface):
        self.screen = screen
        self.list = []

    def draw(self):
        for item in self.list:
            item.draw()

    def move(self, speed: int):
        for item in self.list:
            item.rect.centery += speed
            item.hitbox.centery = item.rect.centery
        self._check_object_delete()

    def _check_object_delete(self):
        for item in self.list:
            if item.rect.y > DP_HEIGHT:
                self.list.remove(item)

    @abstractmethod
    def collision(self, collision_object: Car, time: int):
        ...

    @abstractmethod
    def generate(self):
        ...


class Enemies(RoadObjects):
    def move(self, speed: int):
        for item in self.list:
            if item.ob_rotate:
                item.rect.centery += round(speed * 1.2)
            else:
                item.rect.centery += int(speed / 1.2)
            item.hitbox.centery = item.rect.centery
        self._check_object_delete()

    def generate(self):
        random.seed(tm.time())
        if len(self.list) == 0 or self.list[-1].rect.y > random.randint(DP_HEIGHT//(-45), DP_HEIGHT//9):
            car_model = CARS_PATH[random.randrange(0, len(CARS_PATH))]
            road_line = DP_HEIGHT * (random.randrange(28, 74, 15) / 100) + DP_DELTA
            if road_line < DP_WIDTH / 2:
                self.list.append(RoadObject(self.screen, car_model, road_line, -120, True))
            else:
                self.list.append(RoadObject(self.screen, car_model, road_line, -120, False))

    def collision(self, collision_object: Car, time: int):
        for item in self.list:
            if item.hitbox.colliderect(collision_object.hitbox) and not collision_object.damage_taken:
                if collision_object.health > 1:
                    collision_object.health -= 1
                    collision_object.damage_taken = True
                    collision_object.invulnerable_time_start = time
                elif collision_object.health == 1:
                    end_screen(self.screen)


class Coins(RoadObjects):
    count = 0

    def generate(self):
        random.seed(tm.time())
        if len(self.list) == 0 or self.list[-1].rect.y > DP_HEIGHT//2:
            coin_model = COIN_PATH
            road_line = DP_HEIGHT * (random.randrange(28, 74, 15) / 100) + DP_DELTA
            self.list.append(RoadObject(self.screen, coin_model, road_line, -120))

    def collision(self, collision_object: Car, time: int):
        for item in self.list:
            if item.hitbox.colliderect(collision_object.hitbox):
                self.count += 1
                self.list.remove(item)


def start_screen(screen: pygame.surface, background: Background):
    running = True

    while running:
        screen.fill(GRAY)
        background.draw()

        button_image = pygame.image.load(BUTTON_PATH)
        k_button_widht = button_image.get_rect().width / button_image.get_rect().height
        button_image = pygame.transform.scale(pygame.image.load(BUTTON_PATH),
                                              ((DP_WIDTH // 10) * k_button_widht, DP_HEIGHT // 10))

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

        button_resume = screen.blit(button_image, button_image.get_rect(centerx=DP_WIDTH // 2, bottom=DP_HEIGHT / 2.5))
        button_exit = screen.blit(button_image, button_image.get_rect(centerx=DP_WIDTH // 2, bottom=DP_HEIGHT / 1.8))

        font_object = pygame.font.Font(pygame.font.get_default_font(), 15)

        button_resume_text = font_object.render("Resume", True, WHITE)
        brt_rect = button_resume_text.get_rect(centerx=button_resume.centerx, centery=button_resume.centery)
        button_exit_text = font_object.render("Exit", True, WHITE)
        bet_rect = button_exit_text.get_rect(centerx=button_exit.centerx, centery=button_exit.centery)

        screen.blit(button_resume_text, brt_rect)
        screen.blit(button_exit_text, bet_rect)

        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
            elif button_resume.collidepoint(pygame.mouse.get_pos()):
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

        button_restart = screen.blit(button_image, button_image.get_rect(centerx=DP_WIDTH // 2, bottom=DP_HEIGHT / 2.5))
        button_exit = screen.blit(button_image, button_image.get_rect(centerx=DP_WIDTH // 2, bottom=DP_HEIGHT / 1.8))

        font_object = pygame.font.Font(pygame.font.get_default_font(), 15)

        button_restart_text = font_object.render("Restart", True, WHITE)
        brst_rect = button_restart_text.get_rect(centerx=button_restart.centerx, centery=button_restart.centery)
        button_exit_text = font_object.render("Exit", True, WHITE)
        bet_rect = button_exit_text.get_rect(centerx=button_exit.centerx, centery=button_exit.centery)

        screen.blit(button_restart_text, brst_rect)
        screen.blit(button_exit_text, bet_rect)

        pygame.display.update()
        global SCORE, PREVIOUS_SCORE, BEST_SCORE
        for event in pygame.event.get():
            if button_restart.collidepoint(pygame.mouse.get_pos()):
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    PREVIOUS_SCORE = SCORE
                    if PREVIOUS_SCORE>BEST_SCORE:
                        BEST_SCORE = PREVIOUS_SCORE
                    SCORE = 0
                    magic()
            if button_exit.collidepoint(pygame.mouse.get_pos()):
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    quit()

            if event.type == pygame.QUIT:
                quit()


def show_dev_info(show: bool, screen: pygame.surface, time: float, user_car: Car, background: Background, enemies, coins, frame: int):
    if show:
        font_object = pygame.font.Font(pygame.font.get_default_font(), 15)

        screen.blit(font_object.render(f"Time: {time}", True, BLACK), (10, 10))
        screen.blit(
            font_object.render(f"Speed: {background.speed}, Max: {background.speed % background.max_speed == 0}", True,
                               BLACK), (10, 30))
        screen.blit(font_object.render(f"User car pos: {[user_car.rect.x, user_car.rect.y]}", True, BLACK),
                    (10, 50))
        screen.blit(font_object.render(f"Background Y: {background.rect.y}", True, RED), (10, 70))
        screen.blit(font_object.render(f"Enemies count: {len(enemies.list)}", True, BLACK), (10, 100))
        screen.blit(font_object.render(f"Coins count: {len(coins.list)}", True, BLACK), (10, 120))
        screen.blit(font_object.render(f"Player health: {user_car.health}", True, BLACK), (10, 140))
        screen.blit(font_object.render(f"Player damage taken: {user_car.damage_taken}", True, BLACK), (10, 160))

        if frame % (240/background.speed) == 0:
            screen.blit(font_object.render(f"Frame: {frame}", True, RED), (10, 180))
        else:
            screen.blit(font_object.render(f"Frame: {frame}", True, BLACK), (10, 180))

        for car in enemies.list:
            pygame.draw.rect(screen, BLACK, car.hitbox, 1)
            screen.blit(font_object.render(f"{car.rect.y}", True, WHITE),
                        (car.rect.centerx, car.rect.centery))

        pygame.draw.rect(screen, RED, user_car.hitbox, 1)


def show_player_info(show: bool, screen: pygame.surface, time: int, coins: Coins, user_car: Car, score, background: Background):
    y1 = DP_HEIGHT - 9.5*(DP_HEIGHT/10)
    y2 = DP_HEIGHT - 9*(DP_HEIGHT / 10)
    y3 = DP_HEIGHT - 8.5*(DP_HEIGHT / 10)
    x = DP_WIDTH//10
    sz = (int)(DP_HEIGHT/40)

    if not show:
        font_object = pygame.font.Font(pygame.font.get_default_font(), sz)
        #screen.blit(font_object.render(f"Time: {int(time)}", True, BLACK), (DP_WIDTH/45, DP_HEIGHT//90))
        screen.blit(font_object.render(f"Coins: {coins.count}", True, BLACK), (x, y1))
        screen.blit(font_object.render(f"Health: {user_car.health}", True, RED), (x, y2))
        screen.blit(font_object.render(f"Score: {int(score)}", True, GREEN), (x, y3))


def show_score_info(show: bool, screen: pygame.surface,  previous_score, best_score, background: Background):
    x = DP_WIDTH - 2.2*(DP_WIDTH/10)
    y1 = DP_HEIGHT - 9.5 * (DP_HEIGHT / 10)
    y2 = DP_HEIGHT - 9 * (DP_HEIGHT / 10)
    #y3 = DP_HEIGHT - 8.5 * (DP_HEIGHT / 10)
    sz = (int)(DP_HEIGHT / 40)
    if not show:
        font_object = pygame.font.Font(pygame.font.get_default_font(), (sz))
        #screen.blit(font_object.render(f"Score: {int(score)}", True, GREEN), (x, DP_HEIGHT//90))
        screen.blit(font_object.render(f"Previous score: {int(previous_score)}", True, BLACK), (x, y1))
        screen.blit(font_object.render(f"Best score: {int(best_score)}", True, BLUE), (x, y2))
        #screen.blit(font_object.render(f"Score: {}", True, BLACK), (DP_WIDTH/45, DP_HEIGHT//9))

def magic():

    screen = pygame.display.set_mode((DP_WIDTH, DP_HEIGHT))
    clock = pygame.time.Clock()

    background = Background(screen)
    user_car = Car(screen, CAR_PATH)
    enemies = Enemies(screen)
    coins = Coins(screen)

    frame_count = 0

    global SCORE
    dev_info = False
    running = True
    while running:

        clock.tick(FPS)

        frame_count += 1
        second_count = frame_count / FPS
        SCORE += 0.01*background.speed


        enemies.generate(second_count)
        coins.generate(second_count)

        user_car.make_invulnerable(second_count, frame_count)

        background.move(second_count)
        coins.move(background.speed)
        enemies.move(background.speed)
        user_car.move()

        screen.fill(GRAY)
        background.draw()
        coins.draw()
        enemies.draw()
        user_car.draw()
        show_score_info(dev_info, screen,  PREVIOUS_SCORE,BEST_SCORE,background)
        show_dev_info(dev_info, screen, second_count, user_car, background, enemies, coins)
        show_player_info(dev_info, screen, second_count, coins, user_car, SCORE, background)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_F1:
                    dev_info = not dev_info
                if event.key == pygame.K_ESCAPE:
                    pause_screen(screen)

        pygame.display.update()

        enemies.collision(user_car, second_count)
        coins.collision(user_car, second_count)


        #game()
