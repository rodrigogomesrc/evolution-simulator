class Color(object):

    def __init__(self, r, g, b):
        self.__r = r
        self.__g = g
        self.__b = b

    def get_r(self):
        return self.__r

    def set_r(self, r):
        self.__r = r

    def get_g(self):
        return self.__g

    def set_g(self, g):
        self.__g = g

    def get_b(self):
        return self.__b

    def set_b(self, b):
        self.__b = b

    def get_color(self):
        return self.__r, self.__g, self.__b