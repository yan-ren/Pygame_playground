# This module contains the utility functions in the game
from modules import constants


def calculate_level(score):
    if score < constants.LEVEL_MAP[1]:
        return 1
    elif constants.LEVEL_MAP[1] <= score < constants.LEVEL_MAP[2]:
        return 2
    elif constants.LEVEL_MAP[2] <= score < constants.LEVEL_MAP[3]:
        return 3
    elif constants.LEVEL_MAP[3] <= score < constants.LEVEL_MAP[4]:
        return 4
    elif constants.LEVEL_MAP[4] <= score:
        return 5


def calculate_speed(current_speed, level):
    if current_speed > constants.MAX_SPEED:
        return constants.MAX_SPEED
    else:
        # return current_speed + level
        return current_speed + 2


def crash_detection(car, block):
    if car.y < block.y + block.get_height():
        if block.x < car.x < block.x + block.get_width() or \
                block.x < car.x + car.get_width() < block.x + block.get_width():
            if block.y < car.y < block.y + block.get_height() or \
                    block.y < car.y + car.get_height() < block.y + block.get_height():
                return True
    return False


def level_up(score):
    if score in constants.LEVEL_MAP.values():
        return True
    return False


def convert_time(time):
    """Convert time in millisecond to string format MM:SS:MS"""
    minutes = str(time // 60000).zfill(2)
    second = str((time % 60000) // 1000).zfill(2)
    millisecond = str(time % 1000).zfill(3)
    return "%s:%s:%s" % (minutes, second, millisecond)

