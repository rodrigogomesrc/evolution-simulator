
class Screen(object):

    def __init__(self, width, height, pygame_object):
        self.height = height
        self.width = width
        self.pg = pygame_object

    def render_rectangle(self, window, screen_rectangle, color):
        if window is None or self.pg is None:
            print("\n\n\n\n\n Nada encontrado aqui \n\n\n\n\n\n")
            return

        r, g, b = color.get_color()
        x, y = screen_rectangle.get_position()
        h, w = screen_rectangle.get_size()
        self.pg.draw.rect(window, (r, g, b), (x, y, h, w))
