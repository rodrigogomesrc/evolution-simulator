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

population_record = 0
hungry_deaths = 0
age_deaths = 0

#create initial population
universe.create_food(screen, 100)

for i in range(30):

	velocity = random.randint(30, 100)
	width = random.randint(0, screen.width + 1)
	height = random.randint(0,screen.height + 1)
	universe.create_creature(width, height, screen, velocity)

	velocity = random.randint(30, 100)
	width = random.randint(0, screen.width + 1)
	height = random.randint(0,screen.height + 1)
	universe.create_creature(width, height, screen, velocity)

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

	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			run = False


	reproducted = []
	
	#Move creatures, eat food and check life
	for creature in universe.creatures:

		alive = creature.check_alive()

		# Check life
		if not alive:

			if creature.energy <= 0:
				hungry_deaths += 1

			else:
				age_deaths += 1

			universe.creatures.remove(creature)
			universe.population -= 1
			break

		creature.move()

		# Eat Food
		for food in universe.food:

			dx = abs(food.x_position - creature.x_position)
			dy = abs(food.y_position - creature.y_position)

			if dx <= 20 and dy <= 20:

				universe.food.remove(food)
				creature.eat()
				break

		# Reproduction
		for c in universe.creatures:

			dx = abs(creature.x_position - c.x_position)
			dy = abs(creature.y_position - c.y_position)
			can_reproduce = c.can_reproduce and creature.can_reproduce and creature.idnumber not in reproducted and c.idnumber not in reproducted
			can_reproduce2 = creature.gender != c.gender

			if dx <= 20 and dy <= 20 and dx != 0 and dy != 0 and can_reproduce:

				x = random.randint(0, screen.width + 1)
				y = random.randint(0, screen.height + 1)

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

				universe.create_creature(x, y, screen, velocity, gender=gender)
		
	#Remove food
	for food in universe.food:

		expired = food.expired	

		if expired:
			universe.food.remove(food)

		else:
			food.render()


	print("Population: ", universe.population)

	if universe.population > population_record:
		population_record = universe.population

	if universe.population == 0:
		print("Population extinct")
		run = False

	pygame.display.update()
	    
pygame.quit()
print("Population all times: ", universe.creature_current_id)
print("Population record: ", population_record)
print("Cicles simulated: ", universe.cicles)
print("Hungry deaths: ", hungry_deaths)
print("age_deaths: ", age_deaths)
print("Days simulated: %d" %(universe.cicles / 72))
