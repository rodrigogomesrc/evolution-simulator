import pygame
import random
from screen import Screen
from universe import Universe
from creature import Creature
from food import Food
from timeit import default_timer as timer
import json

class Game(object):

	def __init__(self):

		self.load_configs()
		self.window = pygame.display.set_mode((self.screen.width, self.screen.height))
		self.universe = Universe(self.window, 10, 10, self.screen)
		self.population_record = 0
		self.hungry_deaths = 0
		self.age_deaths = 0
		self.extinction = False
		pygame.display.set_caption('Evolution')
		pygame.init()

		self.cicle_time = 0
		self.total_cicle_time = 0

	def load_configs(self):
		
		with open('config.json') as configs:
			data = json.load(configs)
			self.cicle_size = data['cicleSize']
			self.initial_food = data['initialFood']
			self.initial_creatures = data['initialCreatures']

			width = data['screenWidth']
			height = data['screenHeight']
			self.screen = Screen(width, height)

			self.food_wait = data['ciclesToSpawnFood']
			Food.duration = data['foodDuration']
			self.consider_sex = data['considerTwoSexes']


	def get_random_position(self):
		x = random.randint(0, self.screen.width -1)
		y = random.randint(0, self.screen.height -1)
		return x, y

	def start_world(self):

		print("creating food...")
		for i in range(self.initial_food):
			self.universe.create_food()

		print("creating creatures...")		
		for i in range(self.initial_creatures):
			velocity = random.randint(30, 100)
			if(self.consider_sex):
				creature_sex = random.randint(0, 1)
				self.universe.create_creature(self.screen, velocity, sex=creature_sex)

			else:
				self.universe.create_creature(self.screen, velocity)

		print("food and creatures created, starting simulation..")
		self.cicle_time = timer()

	def spawn_food(self):
		if self.food_wait <= 0:
			self.universe.create_food()
			self.food_wait = 10
		self.food_wait -= 1

	
	def ciclical_checks(self):
		self.spawn_food()
		self.counters()

		if self.universe.population > self.population_record:
			self.population_record = self.universe.population

		if self.universe.population == 0:
			self.extinction = True


	def daily_checks(self, rendering=True):
		if rendering:
			self.window.fill((255, 255, 255))
			self.check_creatures(True)
			self.check_food(True)
			pygame.display.update()
		else:
			self.check_creatures(False)
			self.check_food(False)

		self.evaluate_cicle_time()
		self.print_stats()

	def check_food(self, render):
		food_list = self.universe.food_dict.copy().items()
		if render:
			for id, food in food_list:
				self.check_food_is_expired(food)
				food.render()
		else:
			for id, food in food_list:
				self.check_food_is_expired(food)


	def remove_creature(self, creature):
		self.universe.remove_creature(creature)
		
	def counters(self):
		self.food_wait -= 1
		self.universe.count_cicles()

	def check_if_coordenates_inside_screen(self, x, y):
		if(x >= self.screen.width):
			return False
		elif(y >= self.screen.height):
			return False
		else:
			return True

	def check_creatures_lifes(self, creature):
		alive = creature.check_alive()
		if not alive:

			if creature.energy <= 0:
				self.hungry_deaths += 1

			else:
				self.age_deaths += 1
			self.remove_creature(creature)
		
	def handle_creature_close_to_food(self, creature, x, y):
		removed = self.universe.remove_food_by_position(x, y)
		if removed:
			creature.eat()
			return True
			
		return False

	def check_creature_proximity(self, creature):
		x = creature.get_x()
		y = creature.get_y()

		if(self.check_if_coordenates_inside_screen(x,y)):
			self.handle_creature_close_to_food(creature, x, y)
			self.check_reproduction(creature, x, y)

		if(self.check_if_coordenates_inside_screen(x, y + 1)):
			self.handle_creature_close_to_food(creature, x, y + 1)
			self.check_reproduction(creature, x, y + 1)

		if(self.check_if_coordenates_inside_screen(x, y + -1)):
			self.handle_creature_close_to_food(creature, x, y + -1)
			self.check_reproduction(creature, x, y - 1)

		if(self.check_if_coordenates_inside_screen( x + 1, y)):
			self.handle_creature_close_to_food(creature, x + 1, y)
			self.check_reproduction(creature, x + 1, y)

		if(self.check_if_coordenates_inside_screen(x - 1, y)):
			self.handle_creature_close_to_food(creature, x - 1, y)
			self.check_reproduction(creature, x - 1, y)

		if(self.check_if_coordenates_inside_screen(x - 1, y - 1)):
			self.handle_creature_close_to_food(creature, x - 1, y - 1)
			self.check_reproduction(creature, x - 1, y - 1)

		if(self.check_if_coordenates_inside_screen( x - 1, y + 1)):
			self.handle_creature_close_to_food(creature, x - 1, y + 1)
			self.check_reproduction(creature, x - 1, y + 1)

		if(self.check_if_coordenates_inside_screen(x + 1, y - 1)):
			self.handle_creature_close_to_food(creature, x + 1, y - 1)
			self.check_reproduction(creature, x + 1, y - 1)

		if(self.check_if_coordenates_inside_screen(x - 1, y + 1)):
			self.handle_creature_close_to_food(creature, x - 1, y + 1)
			self.check_reproduction(creature, x - 1, y + 1)
	

	def check_reproduction(self, creature, x, y):

		matrix_id = self.universe.get_creature_matrix_id(x, y)
		if(matrix_id == 0):
			return
		
		if not creature.check_if_able_to_reproduce():
			return
		
		#TODO: logic considering sex
		if self.consider_sex:
			return

		creature_to_reproduce = self.universe.get_creature_by_id(matrix_id)
		new_velocity = creature.get_velocity() + creature_to_reproduce.get_velocity() / 2
		self.universe.create_creature(self.screen, new_velocity)



	def check_food_is_expired(self, food):
		expired = food.is_expired()

		if expired:			
			self.universe.remove_food(food)
			
		else:
			if((game.universe.cicles % 72) == 0):
				food.render()
			

	def check_creatures(self, render=False):

		creatures = self.universe.creatures_dict.copy().items()
		for id, creature in creatures:
			self.check_creatures_lifes(creature)
			self.move_creature(creature, id, render)
			self.check_creature_proximity(creature)


	def move_creature(self, creature, id, render):
		x = creature.get_x()
		y = creature.get_y()
		self.universe.remove_from_creatures_coordenates(x,y)
		x, y = creature.move(render)
		self.universe.add_to_creatures_coordenates(x,y, id)
			

	def loop(self):
		if((game.universe.cicles % self.cicle_size) == 0):
			self.daily_checks(True)			
		else:
			self.check_creatures(False)

		self.ciclical_checks()
		

	def evaluate_cicle_time(self):
		self.total_cicle_time = 0
		self.total_cicle_time = timer() - self.cicle_time
		self.cicle_time = timer()
			

	def print_stats(self):
		print("Population: ", self.universe.population)
		print("Food: ", self.universe.food_count)
		print("Day: %d" %(game.universe.cicles / 72))
		print("Time taken to simulate day (s): %.5f" %(self.total_cicle_time))
		
	    
pygame.quit()

game = Game()
game.start_world()

run = True

while run:
	for event in pygame.event.get():
		if event.type == pygame.QUIT:	
			run = False
	
	game.loop()
	if game.extinction == True:
		pass
		break


print("Population all times: ", game.universe.all_time_population)
print("Population record: ", game.population_record)
print("Cicles simulated: ", game.universe.cicles)
print("Hungry deaths: ", game.hungry_deaths)
print("age_deaths: ", game.age_deaths)
print("Days simulated: %d" %(game.universe.cicles / 72))
