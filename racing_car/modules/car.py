from modules import constants


class Car:
    def __init__(self, x=0.45, y=0.8, x_move=0):
        self.x = constants.WINDOW_WIDTH * x
        self.y = constants.WINDOW_HEIGHT * y
        self.x_move = x_move
        self.x_start = self.x
        self.y_start = self.y

    def restore(self):
        self.x = self.x_start
        self.y = self.y_start
        self.x_move = 0

    def change_x(self):
        self.x += self.x_move

