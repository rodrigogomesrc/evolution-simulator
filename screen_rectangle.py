class ScreenRectangle(object):

    def __init__(self, position_y, position_x, height, width):
        self.__position_y = position_y
        self.__position_x = position_x
        self.__height = height
        self.__width = width

    def get_position_y(self):
        return self.__position_y

    def get_position_x(self):
        return self.__position_x

    def get_height(self):
        return self.__height

    def get_width(self):
        return self.__width

    def set_position_y(self, position_y):
        self.__position_y = position_y

    def set_position_x(self, position_x):
        self.__position_x = position_x

    def set_height(self, height):
        self.__height = height

    def set_width(self, width):
        self.__width = width

    def get_size(self):
        return self.__height, self.__width

    def get_position(self):
        return self.__position_y, self.__position_x