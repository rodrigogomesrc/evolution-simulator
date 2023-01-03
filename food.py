from color import Color
from screen_rectangle import ScreenRectangle


class Food(object):
    determined_duration = None

    def __init__(self, x, y, idnumber):
        self.__x = x
        self.__y = y
        self.__idnumber = idnumber
        self.__duration = Food.determined_duration
        self.__expired = False

    def is_expired(self):
        return self.__expired

    def expire(self):
        self.__duration -= 1

        if self.__duration <= 0:
            self.__expired = True

    def get_id(self):
        return self.__idnumber

    def get_x_position(self):
        return self.__x

    def get_y_position(self):
        return self.__y

    def get_color_object(self):
        return Color(0, 255, 0)

    def get_screen_rectangle(self):
        return ScreenRectangle(self.__x, self.__y, 10, 10)
