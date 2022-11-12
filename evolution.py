import pygame
import random
from screen import Screen
from universe import Universe
from creature import Creature
from food import Food
from timeit import default_timer as timer

class Game(object):

	def __init__(self):

		self.screen = Screen()
		self.window = pygame.display.set_mode((self.screen.width, self.screen.height))
		self.universe = Universe(self.window, 10, 10, self.screen)
		self.population_record = 0
		self.hungry_deaths = 0
		self.age_deaths = 0
		self.food_wait = 1
		self.extinction = False

		pygame.display.set_caption("Evolution")
		pygame.init()

		self.cicle_time = 0
		self.total_cicle_time = 0

	def get_random_position(self):
		x = random.randint(0, self.screen.width -1)
		y = random.randint(0, self.screen.height -1)
		return x, y

	def start_world(self):

		for i in range(100):
			self.universe.create_food()

		print("Quantidade de comida: ", len(self.universe.food_dict.items()))
			
		self.cicle_time = timer()
		
		for i in range(200):
			velocity = random.randint(30, 100)
			x, y = x, y = self.get_random_position()
			self.universe.create_creature(x, y, self.screen, velocity)
		

	def spawn_food(self):
		x, y = self.get_random_position()

		if self.food_wait <= 0:
			self.universe.create_food()
			self.food_wait = 10


	def render_food(self):
		
		food_list = self.universe.food_dict.copy().items()
		print("Quantidade de comida: ", len(self.universe.food_dict.items()))
		for id, food in food_list:
			food.render()

	def remove_food(self, food):
		self.universe.remove_food(food)

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


	def make_creature_eat(self, creature, food_position):
		food = self.universe.food_dict[food_position]
		self.remove_food(food)
		creature.eat()
		
	def handle_creature_close_to_food(self, creature, x, y):
		food_matrix = self.universe.food_position_matrix

		if(self.check_if_coordenates_inside_screen(x,y)):
			food_position = food_matrix[x][y]
			if (food_position != 0 and food_position):
				try:
					self.make_creature_eat(creature, food_position)
					return True
				except:
					pass
			return False


	def check_if_ate(self, creature):
		x = creature.get_x()
		y = creature.get_y()

		ate = self.handle_creature_close_to_food(creature, x, y)
		if(ate):
			return
		ate = self.handle_creature_close_to_food(creature, x, y + 1)
		if(ate):
			return
		ate = self.handle_creature_close_to_food(creature, x, y + -1)
		if(ate):
			return
		ate = self.handle_creature_close_to_food(creature, x + 1, y)
		if(ate):
			return
		ate = self.handle_creature_close_to_food(creature, x - 1, y)
		if(ate):
			return
		ate = self.handle_creature_close_to_food(creature, x - 1, y - 1)
		if(ate):
			return
		ate = self.handle_creature_close_to_food(creature, x + 1, y + 1)
		if(ate):
			return
		ate = self.handle_creature_close_to_food(creature, x + 1, y - 1)
		if(ate):
			return
		ate = self.handle_creature_close_to_food(creature, x - 1, y + 1)


	def check_reproduction(self, creature):

		reproducted = []
			
		for c in self.universe.creatures:

			dx = abs(creature.x_position - c.x_position)
			dy = abs(creature.y_position - c.y_position)
			can_reproduce = c.can_reproduce and creature.can_reproduce and creature.idnumber not in reproducted and c.idnumber not in reproducted
			can_reproduce2 = creature.gender != c.gender

			if dx <= 20 and dy <= 20 and dx != 0 and dy != 0 and can_reproduce:

				x, y = self.get_random_position()
				gender = None
				gender_number = random.randint(0,2)

				if gender_number == 1:
					gender = "M"

				else:
					gender = "F"

				c.time_without_reproduction = 0
				creature.time_without_reproduction = 0
				reproducted.append(creature.idnumber)
				reproducted.append(c.idnumber)

				velocity = (creature.original_velocity + c.original_velocity) / 2

				self.universe.create_creature(x, y, self.screen, velocity, gender=gender)


	def check_food(self):

		for food in self.universe.food:
			expired = food.expired	

			if expired:
				self.remove_food(food)
			

			else:
				if((game.universe.cicles % 72) == 0):
					food.render()


	def checks(self, render=False):

		creatures = self.universe.creatures_dict.copy().items()
		for id, creature in creatures:
			
			self.check_creatures_lifes(creature)
			self.move_creature(creature, id, render)
			self.check_if_ate(creature)
			#self.check_reproduction(creature)
	
		#self.check_food()

	def move_creature(self, creature, id, render):
		x = creature.get_x()
		y = creature.get_y()
		self.universe.remove_from_creatures_coordenates(x,y)
		x, y = creature.move(render)
		self.universe.add_to_creatures_coordenates(x,y,id)
			

	def loop(self):

		if((game.universe.cicles % 72) == 0):
			self.window.fill((255,255,255))
			self.checks(True)
			self.evaluate_cicle_time()
			self.render_food()
			pygame.display.update()
			self.print_stats()
			
		else:
			self.checks(False)

		#self.spawn_food()
		self.counters()

		if self.universe.population > self.population_record:
			self.population_record = self.universe.population

		if self.universe.population == 0:
			self.extinction = True

		

	def evaluate_cicle_time(self):
		self.total_cicle_time = 0
		self.total_cicle_time = timer() - self.cicle_time
		self.cicle_time = timer()
			

	def print_stats(self):
		print("Population: ", self.universe.population)
		print("Day: %d" %(game.universe.cicles / 72))
		print("Time: %.5f" %(self.total_cicle_time))
		
	    
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
		#break



#print("Population all times: ", game.universe.creature_current_id)
print("Population record: ", game.population_record)
print("Cicles simulated: ", game.universe.cicles)
print("Hungry deaths: ", game.hungry_deaths)
print("age_deaths: ", game.age_deaths)
print("Days simulated: %d" %(game.universe.cicles / 72))
