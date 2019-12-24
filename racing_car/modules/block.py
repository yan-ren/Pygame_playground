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
        self.attached = []

    def change_y(self):
        self.y += self.speed

    def random_x(self):
        self.x = random.randint(0, constants.WINDOW_WIDTH - self.img.get_rect().width / 2)

    def get_width(self):
        return self.img.get_rect().width

    def get_height(self):
        return self.img.get_rect().height

    def restore(self):
        self.speed = self.initial_speed
        self.y = self.initial_y
        self.random_x()
        self.attached = []
