# This module contains the utility functions in the game
from racing_car import constants


def calculate_level(score):
    if score < 10:
        return 1
    elif 10 <= score < 20:
        return 2
    elif 20 <= score < 30:
        return 3
    elif 30 <= score < 40:
        return 4
    elif 40 <= score:
        return 5


def calculate_speed(current_speed, level):
    if current_speed > constants.MAX_SPEED:
        return constants.MAX_SPEED
    else:
        return current_speed * level
