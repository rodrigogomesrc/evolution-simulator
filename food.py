import pygame

class Food(object):

	def __init__(self, window, x_position, y_position, idnumber):

		self.window = window
		self.x_position = x_position
		self.y_position = y_position
		self.idnumber = idnumber
		self.duration = 3000

	def render(self):

		self.expire()

		if self.duration > 0:
			pygame.draw.rect(self.window, (0,255,0), (self.x_position, self.y_position, 10, 10))
			return True

		return False

	def expire(self):
		self.duration -= 1
	
