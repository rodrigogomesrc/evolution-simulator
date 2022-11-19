from color import Color
from screen_rectangle import ScreenRectangle


class Food(object):
    duration = None

    def __init__(self, x, y, idnumber):
        self.x = x
        self.y = y
        self.idnumber = idnumber
        self.duration = Food.duration
        self.expired = False

    def is_expired(self):
        return self.expired

    def expire(self):
        self.duration -= 1

        if self.duration <= 0:
            self.expired = True

    def get_id(self):
        return self.idnumber

    def get_x_position(self):
        return self.x

    def get_y_position(self):
        return self.y

    def get_color_object(self):
        return Color(0, 255, 0)

    def get_screen_rectangle(self):
        return ScreenRectangle(self.x, self.y, 10, 10)
