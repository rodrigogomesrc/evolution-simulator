import pygame
import random
from screen import Screen
from universe import Universe
from creature import Creature
from food import Food

class Game(object):

	def __init__(self):

		self.screen = Screen()
		self.window = pygame.display.set_mode((self.screen.width, self.screen.height))
		self.universe = Universe(self.window, 10, 10)
		self.population_record = 0
		self.hungry_deaths = 0
		self.age_deaths = 0
		self.food_wait = 10
		self.extinction = False
		self.position_matrix = []

		self.init_matrix()
		pygame.display.set_caption("Evolution")
		pygame.init()

	def init_matrix(self):
		line = [0 for i in range(self.screen.height)]
		print(len(line))
		self.position_matrix = [line for i in range(self.screen.width)]
		print(len(self.position_matrix))

	def start_world(self):

		self.universe.create_food(self.screen, 100)

		for i in range(100):

			velocity = random.randint(30, 100)
			width = random.randint(0, self.screen.width + 1)
			height = random.randint(0,self.screen.height + 1)
			self.universe.create_creature(width, height, self.screen, velocity)

			velocity = random.randint(30, 100)
			width = random.randint(0, self.screen.width + 1)
			height = random.randint(0, self.screen.height + 1)
			self.universe.create_creature(width, height, self.screen, velocity)

			self.loop()

	def spawn_food(self):

		width = random.randint(0, self.screen.width + 1)
		height = random.randint(0, self.screen.height + 1)

		if self.food_wait <= 0:

			self.universe.create_food(self.screen, 1)
			self.food_wait = 10

		
	def counters(self):
		self.food_wait -= 1
		self.universe.count_cicles()


	def check_creatures_lifes(self, creature):

		alive = creature.check_alive()

		if not alive:

			if creature.energy <= 0:
				self.hungry_deaths += 1

			else:
				self.age_deaths += 1

			self.universe.creatures.remove(creature)
			self.universe.population -= 1


	def check_if_ate(self, creature):

		for food in self.universe.food:

			dx = abs(food.x_position - creature.x_position)
			dy = abs(food.y_position - creature.y_position)

			if dx <= 20 and dy <= 20:

				self.universe.food.remove(food)
				creature.eat()
				break


	def check_reproduction(self, creature):
		
		reproducted = []
			
		for c in self.universe.creatures:

			dx = abs(creature.x_position - c.x_position)
			dy = abs(creature.y_position - c.y_position)
			can_reproduce = c.can_reproduce and creature.can_reproduce and creature.idnumber not in reproducted and c.idnumber not in reproducted
			can_reproduce2 = creature.gender != c.gender

			if dx <= 20 and dy <= 20 and dx != 0 and dy != 0 and can_reproduce:

				x = random.randint(0, self.screen.width + 1)
				y = random.randint(0, self.screen.height + 1)

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
				self.universe.food.remove(food)

			else:
				food.render()


	def checks(self, render=False):

		for creature in self.universe.creatures:
			
			self.check_creatures_lifes(creature)
			creature.move(render)
			self.check_if_ate(creature)
			self.check_reproduction(creature)
	
		self.check_food()


	def loop(self):


		if((game.universe.cicles % 72) == 0):
			self.window.fill((255,255,255))

		self.spawn_food()
		self.counters()
		

		if((game.universe.cicles % 72) == 0):
			self.checks(True)
			print("Population: ", self.universe.population)
			print("Day: %d" %(game.universe.cicles / 72))

		else:
			self.checks(False)

		if self.universe.population > self.population_record:
			self.population_record = self.universe.population

		if self.universe.population == 0:
			self.extinction = True

		if((game.universe.cicles % 72) == 0):
			pygame.display.update()
			
	    
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
		break


print("Population all times: ", game.universe.creature_current_id)
print("Population record: ", game.population_record)
print("Cicles simulated: ", game.universe.cicles)
print("Hungry deaths: ", game.hungry_deaths)
print("age_deaths: ", game.age_deaths)
print("Days simulated: %d" %(game.universe.cicles / 72))
