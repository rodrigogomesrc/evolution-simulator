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
	universe.count_cicles()

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
print("Population all times: ", universe.creature_current_id + 1)
print("Cicles: ", universe.cicles)