import pygame


class Screen(object):

    def __init__(self, width, height):
        self.height = height
        self.width = width

    def render_rectangle(self, window, screen_rectangle, color):
        r, g, b = color.get_color()
        x, y = screen_rectangle.get_position()
        h, w = screen_rectangle.get_size()
        pygame.draw.rect(window, (r, g, b), (x, y, h, w))
