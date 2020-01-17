import pygame
import random
from screen import Screen
from universe import Universe
from creature import Creature
from food import Food

screen = Screen()
window = pygame.display.set_mode((screen.width, screen.height))
universe = Universe(window, 10, 10)
pygame.init()

pygame.display.set_caption("Evolution")

max_population = 0
#create initial population
universe.create_food(screen, 100)

for i in range(4):

	width = random.randint(0, screen.width + 1)
	height = random.randint(0,screen.height + 1)
	universe.create_creature(width, height, screen, 100)
	width = random.randint(0, screen.width + 1)
	height = random.randint(0,screen.height + 1)
	universe.create_creature(width, height, screen, 100)

food_wait = 10

run = True
while run:

	window.fill((255,255,255))

	width = random.randint(0, screen.width + 1)
	height = random.randint(0,screen.height + 1)


	if food_wait <= 0:

		universe.create_food(screen, 1)
		food_wait = 10

	food_wait -= 1

	universe.count_cicles()

	#pygame.time.delay(5)

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

		# change it to be as clean as the reproduction part

		creature_x = creature.x_position
		creature_y = creature.y_position


		# Eat Food
		for food in universe.food:

			food_x = food.x_position
			food_y = food.y_position

			if (abs(food_x - creature_x) <= 20) and (abs(food_y - creature_y) <= 20):

				universe.food.remove(food)
				break

	# Reproduction

	for creature in universe.creatures:

		for c in universe.creatures:

			dx = abs(creature.x_position - c.x_position)
			dy = abs(creature.y_position - c.y_position)

			if dx <= 20 and dy <= 20 and dx != 0 and dy != 0 and c.can_reproduce and creature.can_reproduce:

				# make it so the male can alway reproduce and the female has a time until reproduction is alowed again

				x = random.randint(0, screen.width + 1)
				y = random.randint(0,screen.height + 1)

				c.can_reproduce = False
				creature.can_reproduce = False
				universe.create_creature(x, y, screen, 100)

	#Remove food
	for food in universe.food:

		edible = food.render()		
		if not edible:

			universe.food.remove(food)

	if universe.population > max_population:
		max_population = universe.population

	print("Population: ", universe.population)
	pygame.display.update()

	    
pygame.quit()
print("Population all times: ", universe.creature_current_id)
