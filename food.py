import pygame

class Food(object):

	def __init__(self, window, x_position, y_position, idnumber):

		self.window = window
		self.x_position = x_position
		self.y_position = y_position
		self.idnumber = idnumber
		self.duration = 3000
		self.expired = False

	def render(self):

		self.expire()
		pygame.draw.rect(self.window, (0,255,0), (self.x_position, self.y_position, 10, 10))

	def expire(self):

		self.duration -= 1

		if self.duration <= 0:
			self.expired = True
	
