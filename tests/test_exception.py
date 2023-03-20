import pytest


def test_attribute_exception(game_imitation):
    with pytest.raises(AttributeError):
        game_imitation["user"].check_collision(0)
