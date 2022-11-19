import pygame
import random
from screen import Screen
from universe import Universe
from food import Food
from timeit import default_timer as timer
import json
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

import warnings

warnings.filterwarnings('ignore')  # setting ignore as a parameter


class Game(object):

    def __init__(self):

        self.consider_sex = None
        self.food_wait = None
        self.screen = None
        self.initial_creatures = None
        self.initial_food = None
        self.cicle_size = None
        self.load_configs()
        self.window = pygame.display.set_mode((self.screen.width, self.screen.height))
        self.universe = Universe(self.window, 10, 10, self.screen)
        self.population_record = 0
        self.hungry_deaths = 0
        self.age_deaths = 0
        self.extinction = False
        pygame.display.set_caption('Evolution Simulator')
        pygame.init()

        self.cicle_time = 0
        self.total_cicle_time = 0

        self.simulation_velocity = np.array([])

        self.average_velocity = pd.DataFrame(columns=['velocity', 'day'])
        self.average_age = pd.DataFrame(columns=['age', 'day'])

        self.day_velocities = np.array([])
        self.day_ages = np.array([])

        self.population_limit = 1000

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
        x = random.randint(0, self.screen.width - 1)
        y = random.randint(0, self.screen.height - 1)
        return x, y

    def render_rood(self, food):
        rectangle = food.get_screen_rectangle()
        color = food.get_color_object()
        self.screen.render_rectangle(self.window, rectangle, color)

    def render_creature(self, creature):
        rectangle = creature.get_screen_rectangle()
        color = creature.get_color_object()
        self.screen.render_rectangle(self.window, rectangle, color)

    def start_world(self):

        print("creating food...")
        for i in range(self.initial_food):
            self.universe.create_food()

        print("creating creatures...")
        for i in range(self.initial_creatures):
            velocity = random.randint(30, 100)
            if self.consider_sex:
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
        self.check_creatures()

        if self.universe.population > self.population_record:
            self.population_record = self.universe.population

        if self.universe.population == 0:
            self.extinction = True

    def daily_checks(self):
        self.window.fill((255, 255, 255))
        self.life_checks()
        self.check_creatures(True)
        pygame.display.update()
        self.compute_stats()
        self.evaluate_cicle_time()
        self.print_stats()
        self.clear_day_data()

    def compute_stats(self):
        day = int(game.universe.cicles / self.cicle_size)
        self.average_velocity = pd.concat([self.average_velocity, pd.DataFrame(
            {'velocity': [self.day_velocities.mean()], 'day': [day]})])

        self.average_age = pd.concat([self.average_age, pd.DataFrame(
            {'age': [self.day_ages.mean()], 'day': [day]})])

    def clear_day_data(self):
        self.day_velocities = np.array([])
        self.day_ages = np.array([])

    def life_checks(self):
        self.check_food(True)
        self.check_creatures_lives()

    def check_creatures_lives(self):
        creatures = self.universe.creatures_dict.copy().items()
        for creature_id, creature in creatures:
            self.check_creature_life(creature)

    def check_food(self, render):
        food_list = self.universe.food_dict.copy().items()
        for food_id, food in food_list:
            if render:
                self.render_rood(food)
            self.check_food_is_expired(food)

    def remove_creature(self, creature):
        self.universe.remove_creature(creature)

    def counters(self):
        self.food_wait -= 1
        self.universe.count_cicles()

    def check_if_coordenates_inside_screen(self, x, y):
        if x >= self.screen.width:
            return False
        elif y >= self.screen.height:
            return False
        else:
            return True

    def check_creature_life(self, creature):
        # print("creature velocity: ", creature.velocity)
        alive = creature.is_alive()
        self.day_ages = np.append(self.day_ages, int(creature.age / self.cicle_size))
        self.day_velocities = np.append(self.day_velocities, creature.get_velocity())
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

        if self.check_if_coordenates_inside_screen(x, y):
            self.handle_creature_close_to_food(creature, x, y)
            self.check_reproduction(creature, x, y)

        if self.check_if_coordenates_inside_screen(x, y + 1):
            self.handle_creature_close_to_food(creature, x, y + 1)
            self.check_reproduction(creature, x, y + 1)

        if self.check_if_coordenates_inside_screen(x, y + -1):
            self.handle_creature_close_to_food(creature, x, y + -1)
            self.check_reproduction(creature, x, y - 1)

        if self.check_if_coordenates_inside_screen(x + 1, y):
            self.handle_creature_close_to_food(creature, x + 1, y)
            self.check_reproduction(creature, x + 1, y)

        if self.check_if_coordenates_inside_screen(x - 1, y):
            self.handle_creature_close_to_food(creature, x - 1, y)
            self.check_reproduction(creature, x - 1, y)

        if self.check_if_coordenates_inside_screen(x - 1, y - 1):
            self.handle_creature_close_to_food(creature, x - 1, y - 1)
            self.check_reproduction(creature, x - 1, y - 1)

        if self.check_if_coordenates_inside_screen(x - 1, y + 1):
            self.handle_creature_close_to_food(creature, x - 1, y + 1)
            self.check_reproduction(creature, x - 1, y + 1)

        if self.check_if_coordenates_inside_screen(x + 1, y - 1):
            self.handle_creature_close_to_food(creature, x + 1, y - 1)
            self.check_reproduction(creature, x + 1, y - 1)

        if self.check_if_coordenates_inside_screen(x - 1, y + 1):
            self.handle_creature_close_to_food(creature, x - 1, y + 1)
            self.check_reproduction(creature, x - 1, y + 1)

    def check_reproduction(self, creature, x, y):

        if self.universe.population > self.population_limit:
            return

        matrix_id = self.universe.get_creature_matrix_id(x, y)
        if not creature.check_if_able_to_reproduce():
            return

        # TODO: logic considering sex
        if self.consider_sex:
            return

        try:
            creature_to_reproduce = self.universe.get_creature_by_id(matrix_id)

        except KeyError:
            return

        new_velocity = creature.get_velocity() + creature_to_reproduce.get_velocity() / 2
        self.universe.create_creature(self.screen, new_velocity)

    def check_food_is_expired(self, food):
        food.expire()
        expired = food.is_expired()
        if expired:
            self.universe.remove_food(food)

    def check_creatures(self, render=False):
        creatures = self.universe.creatures_dict.copy().items()
        for creature_id, creature in creatures:
            self.move_creature(creature, creature_id)
            self.check_creature_proximity(creature)

            if render:
                self.render_creature(creature)

    def move_creature(self, creature, creature_id):
        x = creature.get_x()
        y = creature.get_y()
        self.universe.remove_from_creatures_coordenates(x, y)
        x, y = creature.move()
        self.universe.add_to_creatures_coordenates(x, y, creature_id)

    def loop(self):
        if (game.universe.cicles % self.cicle_size) == 0:
            self.daily_checks()

        self.ciclical_checks()

    def evaluate_cicle_time(self):
        self.total_cicle_time = 0
        self.total_cicle_time = timer() - self.cicle_time
        self.cicle_time = timer()

    def print_stats(self):
        objects = self.universe.food_count + self.universe.population
        velocity = (self.total_cicle_time / objects) * 1000
        day = game.universe.cicles / self.cicle_size
        average_creature_velocity = self.average_velocity.iloc[-1]['velocity']
        average_creature_age = self.average_age.iloc[-1]['age']
        self.simulation_velocity = np.append(self.simulation_velocity, velocity)

        print("Population: ", self.universe.population)
        print("Food: ", self.universe.food_count)
        print("Day: %d" % day)
        print("Average creature age: %d days" % average_creature_age)
        print("Average creature velocity: %d" % average_creature_velocity)
        print("Time taken to simulate day (s): %.5f" % self.total_cicle_time)
        print("Velocity to simulate (s/obj): %.5f" % velocity)


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

simulation_average_velocity = np.average(game.simulation_velocity)
print("Population all times: ", game.universe.all_time_population)
print("Population record: ", game.population_record)
print("Cicles simulated: ", game.universe.cicles)
print("Hungry deaths: ", game.hungry_deaths)
print("age_deaths: ", game.age_deaths)
print("Days simulated: %d" % (game.universe.cicles / game.cicle_size))
print("Average simulation velocity (s/obj): %.5f" % simulation_average_velocity)

# plot average_creature_velocity and age_death_age by day with matplotlib

'''
plt.plot(game.average_velocity['day'], game.average_velocity['velocity'], label='Average velocity')
plt.plot(game.average_age['day'], game.average_age['age'], label='Average death age')
plt.show()
'''
