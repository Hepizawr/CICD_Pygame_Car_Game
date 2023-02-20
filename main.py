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
magic()


