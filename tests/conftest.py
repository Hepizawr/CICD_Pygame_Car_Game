import pytest
from game_items import *


@pytest.fixture(autouse=True)
def game_imitation():
    # pygame.init()
    screen = pygame.display.set_mode((DP_WIDTH, DP_HEIGHT))
    clock = pygame.time.Clock()

    background = Background(screen)
    user_car = Car(screen, CAR_PATH)
    enemies = Enemies(screen)
    coins = Coins(screen)

    return {"background": background, "user": user_car, "enemies": enemies, "coins": coins}
