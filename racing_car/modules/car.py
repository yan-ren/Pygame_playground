from modules import constants


class Car:
    def __init__(self, id, img, x=constants.WINDOW_WIDTH * 0.45, y=constants.WINDOW_HEIGHT * 0.8):
        self.id = id
        self.img = img
        self.x = x
        self.y = y
        self.x_move = 0
        self.y_move = 0
        self.x_start = self.x
        self.y_start = self.y
        self.life = 3

    def restore(self):
        self.x = self.x_start
        self.y = self.y_start
        self.x_move = 0
        self.y_move = 0
        self.life = 3

    def change_x(self):
        self.x += self.x_move

    def change_y(self):
        self.y += self.y_move

    def get_width(self):
        return self.img.get_rect().width

    def get_height(self):
        return self.img.get_rect().height

    def __eq__(self, other):
        return self.id == other.id

    def __ne__(self, other):
        return self.id != other.id