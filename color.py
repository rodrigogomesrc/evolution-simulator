class Color(object):

    def __init__(self, r, g, b):
        self.r = r
        self.g = g
        self.b = b

    def get_r(self):
        return self.r

    def set_r(self, r):
        self.r = r

    def get_g(self):
        return self.g

    def set_g(self, g):
        self.g = g

    def get_b(self):
        return self.b

    def set_b(self, b):
        self.b = b

    def get_color(self):
        return self.r, self.g, self.b