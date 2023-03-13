import pytest
from game_config import *
from game_items import RoadObject


@pytest.mark.parametrize("user_car, enemy_car, result",
                         [(RoadObject(0, CAR), RoadObject(0, CAR), True),
                          (RoadObject(0, CAR, ob_bottom=DP_HEIGHT // 2),
                           RoadObject(0, CAR, ob_bottom=(DP_HEIGHT // 2) - 80), True),
                          (RoadObject(0, CAR, ob_bottom=DP_HEIGHT // 2),
                           RoadObject(0, CAR, ob_bottom=(DP_HEIGHT // 2) + 80), True),
                          (RoadObject(0, CAR),
                           RoadObject(0, CAR, ob_centerx=(DP_WIDTH // 2) - 40), True),
                          (RoadObject(0, CAR),
                           RoadObject(0, CAR, ob_centerx=(DP_WIDTH // 2) + 40), True),
                          (RoadObject(0, CAR, ob_bottom=DP_HEIGHT // 2),
                           RoadObject(0, CAR, ob_bottom=(DP_HEIGHT // 2) - 240), False),
                          (RoadObject(0, CAR),
                           RoadObject(0, CAR, ob_centerx=(DP_WIDTH // 2) + 120), False)])
def test_collision_cars(user_car, enemy_car, result):
    assert enemy_car.check_collision(user_car) == result
