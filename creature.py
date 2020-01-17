import random
import pygame

class Creature(object):
	
	def __init__(self, window, x_position, y_position, screen_x, screen_y, velocity, size, idnumber, gender):

		self.window = window
		self.x_position = x_position
		self.y_position = y_position
		self.y_position = y_position
		self.x_position = x_position
		self.screen_x = screen_x
		self.screen_y = screen_y
		self.velocity = 100 - velocity
		self.life = 7200
		self.size = size
		self.moving = False
		self.steps = 0
		self.walking_direction = 0
		self.energy = 500
		self.wait = ((100 - velocity) % 10)
		self.idnumber = idnumber
		self.alive = True
		self.cicles = 0
		self.energy_expended = (velocity % 10)
		self.gender = gender
		self.can_reproduce = True
		self.reproduction_wait = 1500
		self.reproduction_age_start = 2000
		self.reproduction_age_end = 6500
		#create rules to if the creature can reproduce
		#rules by age and energy

	def move(self):

		self.age()
		self.use_energy(self.energy_expended)
		self.check_reproduction()
		self.cicles += 1

		if self.wait <= 0:

			moved = True

			if(self.steps == 0):

				self.walking_direction = random.randint(1,9)
				self.steps = random.randint(10,120)

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

			self.wait = ((100 - self.velocity) % 10)

		self.wait -= 1

		pygame.draw.rect(self.window, (0,0,255), (self.x_position, self.y_position, 10, 10))	


	def move_up(self):

		if(self.y_position + 1 < self.screen_y):
			self.y_position += 1
			return True

		return False

	def move_down(self):

		if(self.y_position - 1 > 0):
			self.y_position -= 1
			return True

		return False

	def move_right(self):

		if self.x_position + 1 < self.screen_x:
			self.x_position += 1
			return True

		return False

	def move_left(self):

		if self.x_position - 1 > 0:
			self.x_position -= 1
			return True

		return False

	def move_right_up(self):

		if(self.y_position + 1 < self.screen_y and self.x_position + 1 < self.screen_x):
			self.y_position += 1
			self.x_position += 1
			return True

		return False

	def move_right_down(self):

		if(self.y_position - 1 > 0 and self.x_position + 1 < self.screen_x):
			self.y_position -= 1
			self.x_position += 1
			return True

		return False

	def move_left_up(self):

		if(self.y_position + 1 < self.screen_y and self.x_position - 1 > 0):
			self.y_position += 1
			self.x_position -= 1
			return True

		return False

	def move_left_down(self):

		if(self.y_position - 1 > 0 and self.x_position - 1 > 0):
			self.y_position -= 1
			self.x_position -= 1
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

	def check_reproduction(self):

		if not self.can_reproduce:
			self.reproduction_wait -= 1

		if self.reproduction_wait == 0:
			self.can_reproduce = True
			self.reproduction_wait = 2000 
