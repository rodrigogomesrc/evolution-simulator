class ScreenRectangle(object):

    def __init__(self, position_y, position_x, height, width):
        self.position_y = position_y
        self.position_x = position_x
        self.height = height
        self.width = width

    def get_position_y(self):
        return self.position_y

    def get_position_x(self):
        return self.position_x

    def get_height(self):
        return self.height

    def get_width(self):
        return self.width

    def set_position_y(self, position_y):
        self.position_y = position_y

    def set_position_x(self, position_x):
        self.position_x = position_x

    def set_height(self, height):
        self.height = height

    def set_width(self, width):
        self.width = width

    def get_size(self):
        return self.height, self.width

    def get_position(self):
        return self.position_y, self.position_x