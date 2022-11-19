import random
import pygame
from creature import Creature
from food import Food


class Universe(object):

    def __init__(self, window, velocity, creatures_size, screen):

        self.window = window
        self.velocity = velocity
        self.creatures_size = creatures_size
        self.population = 0
        self.all_time_population = 0
        self.food_count = 0
        self.cicles = 0
        self.screen = screen

        # creature data
        self.creatures_dict = {}
        self.position_matrix = []
        self.creatures_available_positions = set()

        # food data
        self.food_dict = {}
        self.food_position_matrix = []
        self.food_available_positions = set()

        self.init_matrix()
        self.init_available_positions()

        self.current_id = 0

    def get_id(self):
        self.current_id += 1
        return str(self.current_id)

    # initialize available positions based on tuples of the screen size
    def init_available_positions(self):
        for x in range(self.screen.width):
            for y in range(self.screen.height):
                self.creatures_available_positions.add((x, y))
                self.food_available_positions.add((x, y))

    def get_random_position(self):
        x = random.randint(0, self.screen.width - 1)
        y = random.randint(0, self.screen.height - 1)
        return x, y

    def remove_from_creatures_coordenates(self, x, y):
        self.position_matrix[x][y] = 0

    def add_to_creatures_coordenates(self, x, y, creature_id):
        self.position_matrix[x][y] = creature_id

    def get_food_id_by_position(self, x, y):
        return self.food_position_matrix[x][y]

    def remove_food_by_position(self, x, y):
        food_id = self.food_position_matrix[x][y]
        return self.remove_food_by_id(food_id)

    def remove_food_by_id(self, food_id):
        if food_id in self.food_dict.keys():
            food = self.food_dict[food_id]
            self.remove_food(food)
            return True

        return False

    def remove_food(self, food):
        food_id = food.get_id()

        del self.food_dict[food_id]

        food_y = food.get_y_position()
        food_x = food.get_x_position()

        self.food_position_matrix[food_x][food_y] = None

        self.food_count -= 1
        self.food_available_positions.add((food_x, food_y))

    def remove_creature(self, creature):
        creature_id = creature.get_id()
        del self.creatures_dict[creature_id]
        self.position_matrix[creature.get_x()][creature.get_y()] = None
        self.population -= 1
        self.creatures_available_positions.add((creature.get_x(), creature.get_y()))

    def init_matrix(self):
        line = [0 for i in range(self.screen.height)]
        line_food = [0 for i in range(self.screen.height)]
        self.position_matrix = [line for i in range(self.screen.width)]
        self.food_position_matrix = [line_food for i in range(self.screen.width)]

    def count_cicles(self):
        self.cicles += 1

    def create_creature(self, screen, velocity, sex=None):

        if not len(self.food_available_positions) > 0:
            return

        x, y = self.get_random_position()

        while (x, y) not in self.creatures_available_positions:
            x, y = self.get_random_position()

        id = self.get_id()

        if sex:
            new_creature = Creature(x, y, screen.width,
                                    screen.height, velocity, self.creatures_size, id, sex)
        else:
            creature_sex = None
            new_creature = Creature(x, y, screen.width, screen.height,
                                    velocity, self.creatures_size, id, creature_sex)

        self.creatures_dict[id] = new_creature
        self.position_matrix[x][y] = id
        self.population += 1
        self.all_time_population += 1

        self.creatures_available_positions.remove((x, y))

        pygame.draw.rect(self.window, (0, 0, 255), (x, y, 10, 10))

    def create_food(self):

        # check if there is any available position
        if not len(self.food_available_positions) > 0:
            return

        self.food_count += 1

        x, y = self.get_random_position()

        while (x, y) not in self.food_available_positions:
            x, y = self.get_random_position()

        self.food_available_positions.remove((x, y))

        id = self.get_id()

        new_food = Food(x, y, id)

        self.food_dict[id] = new_food
        self.food_position_matrix[x][y] = id

        pygame.draw.rect(self.window, (0, 255, 0), (x, y, 8, 8))

    def get_creature_matrix_id(self, x, y):
        return self.position_matrix[x][y]

    def get_food_matrix_id(self, x, y):
        return self.food_position_matrix[x][y]

    def get_creature_by_id(self, creature_id):
        return self.creatures_dict[creature_id]

    def get_food_by_id(self, creature_id):
        return self.food_dict[creature_id]
