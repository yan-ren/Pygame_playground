from modules import constants


class Car:
    def __init__(self, img, x=constants.WINDOW_WIDTH * 0.45, y=constants.WINDOW_HEIGHT * 0.8, x_move=0):
        self.img = img
        self.x = x
        self.y = y
        self.x_move = x_move
        self.x_start = self.x
        self.y_start = self.y
        self.life = 3

    def restore(self):
        self.x = self.x_start
        self.y = self.y_start
        self.x_move = 0
        self.life = 3

    def change_x(self):
        self.x += self.x_move

    def get_width(self):
        return self.img.get_rect().width

