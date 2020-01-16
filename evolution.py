import pygame
import random


class Screen(object):
	
	def __init__(self):
		
		self.height = 600
		self.width = 1000

class Universe(object):
	
	def __init__(self, velocity, creatures_size):

		self.velocity = velocity
		self.creatures = []
		self.food = []
		self.creatures_size = creatures_size
		self.population = 0
		self.food_count = 0
		self.food_current_id = 0
		self.creature_current_id = 0

	def create_creature(self, x_position, y_position, screen):

		random_velocity = random.randint(10, 20)
		new_creature = Creature(x_position, y_position, screen.width, screen.height, random_velocity, self.creatures_size, self.creature_current_id)
		self.creatures.append(new_creature)
		self.population += 1
		pygame.draw.rect(window, (0,0,255), (x_position, y_position, 10, 10))	
		self.creature_current_id += 1

	def create_food(self, x_position, y_position, screen, quantity):

		for i in range(quantity):

			new_food = Food(x_position, y_position, self.food_current_id)
			self.food.append(new_food)
			pygame.draw.rect(window, (0,255,0), (x_position, y_position, 10, 10))	
			self.food_current_id += 1


class Food(object):

	def __init__(self, x_position, y_position, idnumber):

		self.x_position = x_position
		self.y_position = y_position
		self.idnumber = idnumber
		self.duration = 100

	def render(self):

		self.expire()

		if self.duration > 0:
			pygame.draw.rect(window, (0,255,0), (self.x_position, self.y_position, 10, 10))
			return True

		return False

	def expire(self):
		self.duration -= 1
	

class Creature(object):
	
	def __init__(self, x_position, y_position, screen_x, screen_y, velocity, size, idnumber):

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

		pygame.draw.rect(window, (0,0,255), (self.x_position, self.y_position, 10, 10))	


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


universe = Universe(10, 10)
screen = Screen()

pygame.init()

window = pygame.display.set_mode((screen.width, screen.height))
pygame.display.set_caption("Evolution")
	

run = True

while run:

	window.fill((255,255,255))

	#Create food and creatures
	width = random.randint(0, screen.width + 1)
	height = random.randint(0,screen.height + 1)

	universe.create_creature(width, height, screen)

	width = random.randint(0, screen.width + 1)
	height = random.randint(0,screen.height + 1)

	universe.create_food(width, height, screen, 2)

	pygame.time.delay(100)

	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			run = False


	
	#Move creatures, eat food and check life
	for creature in universe.creatures:

		alive = creature.check_alive()
		# Check life
		if not alive:

			indice = 0
			for c in universe.creatures:
				if c.idnumber == creature.idnumber:
					universe.creatures.pop(indice)
					universe.population -= 1
					break

				indice += 1

		creature.move()

		creature_x = creature.x_position
		creature_y = creature.y_position


		# Eat Food
		for food in universe.food:

			food_x = food.x_position
			food_y = food.y_position

			if (abs(food_x - creature_x) <= 20) and (abs(food_y - creature_y) <= 20):

				indice = 0
				for f in universe.food:
					if f.idnumber == food.idnumber:
						universe.food.pop(indice)
						creature.energy += 200

				indice += 1


	#Remove food
	for food in universe.food:

		edible = food.render()		
		if not edible:

			indice = 0
			for f in universe.food:
				if f.idnumber == food.idnumber:
					universe.food.pop(indice)

			indice += 1

	print("Population: ", universe.population)
	pygame.display.update()

	    
pygame.quit()