import pytest
from game_items import RoadObject
from game_config import DP_HEIGHT, COIN_PATH


@pytest.mark.parametrize("coin, result",
                         [
                             (RoadObject(0, COIN_PATH, ob_bottom=DP_HEIGHT // 2), True),
                             (RoadObject(0, COIN_PATH, ob_bottom=0), False)
                         ])
def test_coins_append(game_imitation, coin, result):
    game_imitation["coins"].list.append(coin)
    first_coins_count = game_imitation["coins"].count
    game_imitation["coins"].collision_action(game_imitation["user"], 0)
    second_coins_count = game_imitation["coins"].count
    assert (first_coins_count != second_coins_count) == result


def test_coins_exception(game_imitation):
    with pytest.raises(AttributeError):
        game_imitation["user"].check_collision(0)
