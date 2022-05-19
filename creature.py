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
		self.original_velocity = velocity
		self.velocity = 100 - velocity
		self.life = 7200
		self.age = 0
		self.size = size
		self.moving = False
		self.steps = 0
		self.walking_direction = 0
		self.energy = 10000
		self.energy_max = 10000
		self.wait_to_velocity = ((100 - velocity) // 10) 
		self.idnumber = idnumber
		self.alive = True
		self.cicles = 0
		self.energy_expended = (velocity // 30)
		self.gender = gender
		self.can_reproduce = False
		self.time_without_reproduction = 0
		self.reproduction_wait = 1000
		self.reproduction_age_start = 2000
		self.reproduction_age_end = 6500

		self.mutate()

	def mutate(self):

		life_mutation_range = ((random.randint(0, 30) - 15) / 100) * self.life
		self.life += life_mutation_range

		velocity_mutation_range = ((random.randint(0, 30) - 15) / 100) * self.life
		self.velocity += velocity_mutation_range

		if self.velocity < 0:
			self.velocity = 0


	def move(self, render=False):
		
		self.age_creature()
		self.use_energy(self.energy_expended)
		self.check_reproduction()
		self.cicles += 1

		if self.wait_to_velocity <= 0:

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

			self.wait_to_velocity = ((100 - self.velocity) % 10)

		self.wait_to_velocity -= 1

		if(render):
			pygame.draw.rect(self.window, (2 * self.original_velocity, 0, 255), (self.x_position, self.y_position, 10, 10))	


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

	def age_creature(self):

		self.age += 1

		if self.age >= self.life:
			self.alive = False

	def use_energy(self, quantity):
		self.energy -= quantity
		if self.energy <= 0:
			self.alive = False

	def check_alive(self):
		return self.alive

	def get_id(self):
		return self.idnumber

	def get_x_position(self):
		return self.x_position

	def get_y_position(self):
		return self.y_position

	def eat(self):

		if self.energy < self.energy_max:
			self.energy += 50

	def check_reproduction(self):

		self.time_without_reproduction += 1

		if self.time_without_reproduction < self.reproduction_wait:
			self.can_reproduce = False

		elif self.energy < (self.energy_max / 2):
			self.can_reproduce = False

		elif self.age < self.reproduction_age_start:
			self.can_reproduce = False

		elif self.age > self.reproduction_age_end:
			self.can_reproduce = False

		elif self.time_without_reproduction < self.reproduction_wait:
			self.can_reproduce = False

		else:
			self.can_reproduce = True
