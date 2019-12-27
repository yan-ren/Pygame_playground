import random
from modules import constants


class Block:
    def __init__(self, img, x, y, speed=7):
        self.img = img
        self.x = x
        self.y = y
        self.initial_y = y
        self.speed = speed
        self.initial_speed = speed
        self.crashed = False

    def change_y(self):
        self.y += self.speed

    def random_x(self):
        return random.randint(0, constants.WINDOW_WIDTH - self.img.get_rect().width / 2)

    def get_width(self):
        return self.img.get_rect().width

    def get_height(self):
        return self.img.get_rect().height

    def get_height(self):
        return self.img.get_rect().height

    def set_to_top(self):
        self.crashed = False
        self.y = random.randint(-constants.WINDOW_HEIGHT, 0)
        self.x = self.random_x()

