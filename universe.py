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

		self.creatures_dict = {}
		self.food_dict = {}
		self.position_matrix = []
		self.food_position_matrix = []

		self.init_matrix()

	def remove_food(self, food_id):
		pass

	def remove_creature(self, creature_id):
		pass

	def init_matrix(self):
		line = [0 for i in range(self.screen.height)]
		self.position_matrix = [line for i in range(self.screen.width)]
		self.food_position_matrix = self.position_matrix

	def count_cicles(self):

		self.cicles += 1

	def create_creature(self, x_position, y_position, screen, velocity, gender=None):


		if gender:
			new_creature = Creature(self.window, x_position, y_position, screen.width, 
				screen.height, velocity, self.creatures_size, self.creature_current_id, gender)
		else:

			creature_gender = None#print((x, y))
			new_creature = Creature(
				self.window, x_position, y_position, screen.width, screen.height, 
				velocity, self.creatures_size, self.creature_current_id, creature_gender)

		#before implementing dict logic
		self.creatures.append(new_creature)

		#after implementing dict logic
		print((x_position, y_position))
		self.creatures_dict[self.creature_current_id] = new_creature
		self.position_matrix[x_position][y_position] = self.creature_current_id

		self.population += 1
		
		pygame.draw.rect(self.window, (0,0,255), (x_position, y_position, 10, 10))	

		self.creature_current_id += 1

	def create_food(self, x, y):

		#before dict implementation
		new_food = Food(self.window, x, y, self.food_current_id)
		self.food.append(new_food)

		#after dict implementation
		self.food_dict[self.food_current_id] = new_food
		self.food_position_matrix[x][y] = self.food_current_id

		pygame.draw.rect(self.window, (0,255,0), (x, y, 10, 10))	
		self.food_current_id += 1


			
