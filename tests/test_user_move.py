import pygame


def test_user_car_move(game_imitation, monkeypatch):
    input_values = [
        {pygame.K_LEFT: False, pygame.K_RIGHT: True, pygame.K_UP: False, pygame.K_DOWN: False},
        {pygame.K_LEFT: True, pygame.K_RIGHT: False, pygame.K_UP: False, pygame.K_DOWN: False},
        {pygame.K_LEFT: False, pygame.K_RIGHT: False, pygame.K_UP: True, pygame.K_DOWN: False},
        {pygame.K_LEFT: False, pygame.K_RIGHT: False, pygame.K_UP: False, pygame.K_DOWN: True}]

    def get_key_pressed():
        # return input_value
        return input_values.pop(0)

    monkeypatch.setattr('pygame.key.get_pressed', lambda: get_key_pressed())

    start_position = [game_imitation["user"].rect.x, game_imitation["user"].rect.y]

    game_imitation["user"].move()

    assert game_imitation["user"].rect.x > start_position[0]
