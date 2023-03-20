from game_config import DP_HEIGHT
import pytest


# @pytest.mark.skip
@pytest.mark.parametrize("y_move, result",
                         [
                             (DP_HEIGHT//7, True),
                             (0, False)
                         ])
def test_enemy_generate(game_imitation, y_move, result):
    game_imitation["enemies"].generate()
    start_enemy_count = len(game_imitation["enemies"].list)
    game_imitation["enemies"].list[-1].rect.y = y_move
    game_imitation["enemies"].generate()

    assert (len(game_imitation["enemies"].list) == start_enemy_count + 1) == result


@pytest.mark.parametrize("y_move, result",
                         [
                             (DP_HEIGHT * 2, True),
                             (DP_HEIGHT // 3, False)
                         ])
def test_enemy_delete(game_imitation, y_move, result):
    game_imitation["enemies"].generate()

    game_imitation["enemies"].list[-1].rect.y = y_move
    game_imitation["enemies"]._check_object_delete()

    assert (len(game_imitation["enemies"].list) == 0) == result
