import random
from modules import constants


class Block:
    def __init__(self, width, height, color, x, y, speed=7):
        self.width = width
        self.height = height
        self.color = color
        self.x = x
        self.y = y
        self.speed = speed
        self.initial_speed = speed

    def change_y(self):
        self.y += self.speed

    def random_x(self):
        self.x = random.randint(0, constants.WINDOW_WIDTH)