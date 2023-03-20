import pygame
import pytest
from game_items import RoadObject
from game_config import DP_HEIGHT, CAR_PATH


# def test_user_car_move_left(game_imitation, monkeypatch):
#     input_values = {pygame.K_LEFT: True, pygame.K_RIGHT: False, pygame.K_UP: False, pygame.K_DOWN: False}
#
#     def get_key_pressed():
#         return input_values
#
#     monkeypatch.setattr('pygame.key.get_pressed', lambda: get_key_pressed())
#
#     start_position = [game_imitation["user"].rect.x, game_imitation["user"].rect.y]
#
#     game_imitation["user"].move()
#
#     assert game_imitation["user"].rect.x < start_position[0]
#
#
# def test_user_car_move_right(game_imitation, monkeypatch):
#     input_values = {pygame.K_LEFT: False, pygame.K_RIGHT: True, pygame.K_UP: False, pygame.K_DOWN: False}
#
#     def get_key_pressed():
#         return input_values
#
#     monkeypatch.setattr('pygame.key.get_pressed', lambda: get_key_pressed())
#
#     start_position = [game_imitation["user"].rect.x, game_imitation["user"].rect.y]
#
#     game_imitation["user"].move()
#
#     assert game_imitation["user"].rect.x > start_position[0]
#
#
# def test_user_car_move_up(game_imitation, monkeypatch):
#     input_values = {pygame.K_LEFT: False, pygame.K_RIGHT: False, pygame.K_UP: True, pygame.K_DOWN: False}
#
#     def get_key_pressed():
#         return input_values
#
#     monkeypatch.setattr('pygame.key.get_pressed', lambda: get_key_pressed())
#
#     start_position = [game_imitation["user"].rect.x, game_imitation["user"].rect.y]
#
#     game_imitation["user"].move()
#
#     assert game_imitation["user"].rect.y < start_position[1]
#
#
# def test_user_car_move_down(game_imitation, monkeypatch):
#     input_values = {pygame.K_LEFT: False, pygame.K_RIGHT: False, pygame.K_UP: False, pygame.K_DOWN: True}
#
#     def get_key_pressed():
#         return input_values
#
#     monkeypatch.setattr('pygame.key.get_pressed', lambda: get_key_pressed())
#
#     start_position = [game_imitation["user"].rect.x, game_imitation["user"].rect.y]
#
#     game_imitation["user"].move()
#
#     assert game_imitation["user"].rect.y > start_position[1]
#
#
# @pytest.mark.parametrize("input_value",
#                          [{pygame.K_LEFT: True, pygame.K_RIGHT: False, pygame.K_UP: False, pygame.K_DOWN: False},
#                           {pygame.K_LEFT: True, pygame.K_RIGHT: False, pygame.K_UP: True, pygame.K_DOWN: False}])
# def test_user_car_move_horizontal(game_imitation, monkeypatch, input_value):
#     monkeypatch.setattr('pygame.key.get_pressed', lambda: input_value)
#
#     start_position = [game_imitation["user"].rect.x, game_imitation["user"].rect.y]
#
#     game_imitation["user"].move()
#
#     assert game_imitation["user"].rect.x < start_position[0]


@pytest.mark.parametrize("input_value, cord, result",
                         [
                             ({pygame.K_LEFT: True, pygame.K_RIGHT: False, pygame.K_UP: False, pygame.K_DOWN: False},
                              'x', True),
                             ({pygame.K_LEFT: False, pygame.K_RIGHT: True, pygame.K_UP: False, pygame.K_DOWN: False},
                              'x', False),
                             ({pygame.K_LEFT: False, pygame.K_RIGHT: False, pygame.K_UP: True, pygame.K_DOWN: False},
                              'y', True),
                             ({pygame.K_LEFT: False, pygame.K_RIGHT: False, pygame.K_UP: False, pygame.K_DOWN: True},
                              'y', False),
                         ])
def test_user_car_move(game_imitation, monkeypatch, input_value, cord, result):
    monkeypatch.setattr('pygame.key.get_pressed', lambda: input_value)

    first_position = {'x': game_imitation["user"].rect.x, 'y': game_imitation["user"].rect.y}
    game_imitation["user"].move()
    second_position = {'x': game_imitation["user"].rect.x, 'y': game_imitation["user"].rect.y}

    assert (first_position[cord] > second_position[cord]) == result


@pytest.mark.parametrize("enemy_car, result",
                         [
                             (RoadObject(0, CAR_PATH, ob_bottom=DP_HEIGHT // 2), True),
                             (RoadObject(0, CAR_PATH, ob_bottom=DP_HEIGHT // 4), False),
                             (RoadObject(0, CAR_PATH, ob_bottom=DP_HEIGHT), False)
                         ])
def test_user_car_immortal(game_imitation, enemy_car: RoadObject, result):
    first_immortal_bool = game_imitation["user"].immortal
    game_imitation["enemies"].list.append(enemy_car)
    game_imitation["enemies"].collision_action(game_imitation["user"], 0)
    second_immortal_bool = game_imitation["user"].immortal
    assert (first_immortal_bool != second_immortal_bool) == result
