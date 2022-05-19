import random
import pygame
from creature import Creature
from food import Food

class Universe(object):
	
	def __init__(self, window, velocity, creatures_size, screen):

		self.window = window
		self.velocity = velocity
		self.creatures = []
		self.food = []
		self.creatures_size = creatures_size
		self.population = 0
		self.food_count = 0
		self.food_current_id = 0
		self.creature_current_id = 0
		self.cicles = 0
		self.screen = screen
		self.position_matrix = []
		self.init_matrix()

	def init_matrix(self):
		line = [0 for i in range(self.screen.height)]
		self.position_matrix = [line for i in range(self.screen.width)]

	def count_cicles(self):

		self.cicles += 1

	def create_creature(self, x_position, y_position, screen, velocity, gender=None):


		if gender:
			new_creature = Creature(self.window, x_position, y_position, screen.width, 
				screen.height, velocity, self.creatures_size, self.creature_current_id, gender)
		else:

			creature_gender = None
			gender_number = random.randint(1,3)

			if gender_number == 1: 
				creature_gender = "M" 

			else: 
				gender_number = "F"

			new_creature = Creature(
				self.window, x_position, y_position, screen.width, screen.height, 
				velocity, self.creatures_size, self.creature_current_id, creature_gender)

		self.creatures.append(new_creature)
		self.population += 1
		pygame.draw.rect(self.window, (0,0,255), (x_position, y_position, 10, 10))	
		self.creature_current_id += 1

	def create_food(self, screen, quantity):

		for i in range(quantity):

			x = random.randint(0, screen.width + 1)
			y = random.randint(0,screen.height + 1)

			new_food = Food(self.window, x, y, self.food_current_id)
			self.food.append(new_food)
			pygame.draw.rect(self.window, (0,255,0), (x, y, 10, 10))	
			self.food_current_id += 1

