import random
import pygame
from creature import Creature
from food import Food

class Universe(object):
	
	def __init__(self, window, velocity, creatures_size):

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

	def count_cicles(self):
		self.cicles += 1

	def create_creature(self, x_position, y_position, screen):

		random_velocity = random.randint(10, 20)
		new_creature = Creature(self.window, x_position, y_position, screen.width, screen.height, random_velocity, self.creatures_size, self.creature_current_id)
		self.creatures.append(new_creature)
		self.population += 1
		pygame.draw.rect(self.window, (0,0,255), (x_position, y_position, 10, 10))	
		self.creature_current_id += 1

	def create_food(self, x_position, y_position, screen, quantity):

		for i in range(quantity):

			new_food = Food(self.window, x_position, y_position, self.food_current_id)
			self.food.append(new_food)
			pygame.draw.rect(self.window, (0,255,0), (x_position, y_position, 10, 10))	
			self.food_current_id += 1

