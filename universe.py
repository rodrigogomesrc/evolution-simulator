import random
import pygame
from creature import Creature
from food import Food
import uuid

class Universe(object):
	
	def __init__(self, window, velocity, creatures_size, screen):

		self.window = window
		self.velocity = velocity
		self.creatures = []
		self.food = []
		self.creatures_size = creatures_size
		self.population = 0
		self.food_count = 0
		self.cicles = 0
		self.screen = screen

		self.creatures_dict = {}
		self.food_dict = {}
		self.position_matrix = []
		self.food_position_matrix = []

		self.init_matrix()

	def remove_from_creatures_coordenates(self, x, y):
		self.position_matrix[x][y] = 0

	def add_to_creatures_coordenates(self, x, y, creature_id):
		self.position_matrix[x][y] = creature_id

	def remove_food(self, food):
		food_id = food.get_id()
		del self.food_dict[food_id]
		self.food_position_matrix[food.get_x_position()][food.get_y_position()] = 0
		self.food_count -= 1

	def remove_creature(self, creature):
		creature_id = creature.get_id()
		del self.creatures_dict[creature_id]
		self.position_matrix[creature.get_x()][creature.get_y()]
		self.population -= 1

	def init_matrix(self):
		line = [0 for i in range(self.screen.height)]
		self.position_matrix = [line for i in range(self.screen.width)]
		self.food_position_matrix = self.position_matrix

	def count_cicles(self):
		self.cicles += 1

	def create_creature(self, x_position, y_position, screen, velocity, gender=None):

		id = uuid.uuid4()
		if gender:
			new_creature = Creature(self.window, x_position, y_position, screen.width, 
				screen.height, velocity, self.creatures_size, id, gender)
		else:
			creature_gender = None
			new_creature = Creature(
				self.window, x_position, y_position, screen.width, screen.height, 
				velocity, self.creatures_size, id, creature_gender)

		self.creatures_dict[id] = new_creature
		self.position_matrix[x_position][y_position] = id
		self.population += 1
		
		pygame.draw.rect(self.window, (0,0,255), (x_position, y_position, 10, 10))	

	def create_food(self, x, y):
		id = uuid.uuid4()
		new_food = Food(self.window, x, y, id)
		self.food_dict[id] = new_food
		self.food_position_matrix[x][y] = id

		pygame.draw.rect(self.window, (0,255,0), (x, y, 8, 8))


			
