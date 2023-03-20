import pytest
from game_items import *


@pytest.fixture(autouse=True)
def game_imitation():
    screen = pygame.display.set_mode((DP_WIDTH, DP_HEIGHT))

    background = Background(screen)
    user_car = Car(screen, CAR_PATH, ob_bottom=DP_HEIGHT // 2)
    enemies = Enemies(screen)
    coins = Coins(screen)

    return {"background": background, "user": user_car, "enemies": enemies, "coins": coins}
