import random
import pygame

class Creature(object):
	
	def __init__(self, window, x_position, y_position, screen_x, screen_y, velocity, size, idnumber):

		self.window = window
		self.x_position = x_position
		self.y_position = y_position
		self.y_position = y_position
		self.x_position = x_position
		self.screen_x = screen_x
		self.screen_y = screen_y
		self.velocity = velocity
		self.life = 100
		self.size = size
		self.moving = False
		self.steps = 0
		self.walking_direction = 0
		self.energy = 1000
		self.idnumber = idnumber
		self.alive = True
		self.cicles = 0

	def move(self):

		self.age()
		self.use_energy(self.velocity)
		self.cicles += 1
		moved = True

		if(self.steps == 0):

			self.walking_direction = random.randint(1,9)
			self.steps = random.randint(1,11)

		else:
			self.steps -= 1

		if(self.walking_direction == 1):
			moved = self.move_up()

		if(self.walking_direction == 2):
			moved = self.move_down()

		if(self.walking_direction == 3):
			moved = self.move_right()

		if(self.walking_direction == 4):
			moved = self.move_left()

		if(self.walking_direction == 5):
			moved = self.move_right_up()

		if(self.walking_direction == 6):
			moved = self.move_right_down()

		if(self.walking_direction == 7):
			moved = self.move_left_up()

		if(self.walking_direction == 8):
			moved = self.move_left_down()

		if not moved:
			self.steps = 0

		pygame.draw.rect(self.window, (0,0,255), (self.x_position, self.y_position, 10, 10))	


	def move_up(self):

		if(self.y_position + self.velocity < self.screen_y):
			self.y_position += self.velocity
			return True

		return False

	def move_down(self):

		if(self.y_position - self.velocity > 0):
			self.y_position -= self.velocity
			return True

		return False

	def move_right(self):

		if self.x_position + self.velocity < self.screen_x:
			self.x_position += self.velocity
			return True

		return False

	def move_left(self):

		if self.x_position - self.velocity > 0:
			self.x_position -= self.velocity
			return True

		return False

	def move_right_up(self):

		if(self.y_position + self.velocity < self.screen_y and self.x_position + self.velocity < self.screen_x):
			self.y_position += self.velocity
			self.x_position += self.velocity
			return True

		return False

	def move_right_down(self):

		if(self.y_position - self.velocity > 0 and self.x_position + self.velocity < self.screen_x):
			self.y_position -= self.velocity
			self.x_position += self.velocity
			return True

		return False

	def move_left_up(self):

		if(self.y_position + self.velocity < self.screen_y and self.x_position - self.velocity > 0):
			self.y_position += self.velocity
			self.x_position -= self.velocity
			return True

		return False

	def move_left_down(self):

		if(self.y_position - self.velocity > 0 and self.x_position - self.velocity > 0):
			self.y_position -= self.velocity
			self.x_position -= self.velocity
			return True

		return False

	def age(self):

		self.life -= 1

		if self.life <= 0:
			self.alive = False

	def use_energy(self, quantity):

		self.energy -= quantity

		if self.energy <= 0:
			self.alive = False

	def check_alive(self):

		return self.alive
