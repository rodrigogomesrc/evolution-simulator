import random
from creature import Creature
from food import Food


class Universe(object):

    def __init__(self, window, velocity, creatures_size, screen, pygame_object):

        self.__pg = pygame_object
        self.__window = window
        self.__velocity = velocity
        self.__creatures_size = creatures_size
        self.__population = 0
        self.__all_time_population = 0
        self.__food_count = 0
        self.__cicles = 0
        self.__screen = screen

        # creature data
        self.__creatures_dict = {}
        self.__position_matrix = []
        self.__creatures_available_positions = set()

        # food data
        self.__food_dict = {}
        self.__food_position_matrix = []
        self.__food_available_positions = set()

        self.init_matrix()
        self.init_available_positions()

        self.__current_id = 0
        self.__render = True

        if window is None or pygame_object is None:
            self.__render = False

    def get_id(self):
        self.__current_id += 1
        return str(self.__current_id)

    def get_food_count(self):
        return self.__food_count

    def get_population(self):
        return self.__population

    def get_all_time_population(self):
        return self.__all_time_population

    def get_cicles(self):
        return self.__cicles

    def get_cicle_size(self):
        return len(self.__creatures_dict)

    def get_food_dict(self):
        return self.__food_dict

    def get_creature_dict(self):
        return self.__creatures_dict

    def get_population(self):
        return self.__population

    def get_food_count(self):
        return self.__food_count

    def init_available_positions(self):
        for x in range(self.__screen.get_width()):
            for y in range(self.__screen.get_height()):
                self.__creatures_available_positions.add((x, y))
                self.__food_available_positions.add((x, y))

    def get_random_position(self):
        x = random.randint(0, self.__screen.get_width() - 1)
        y = random.randint(0, self.__screen.get_height() - 1)
        return x, y

    def remove_from_creatures_coordenates(self, x, y):
        self.__position_matrix[x][y] = 0

    def add_to_creatures_coordenates(self, x, y, creature_id):
        self.__position_matrix[x][y] = creature_id

    def get_food_id_by_position(self, x, y):
        return self.__food_position_matrix[x][y]

    def remove_food_by_position(self, x, y):
        food_id = self.__food_position_matrix[x][y]
        return self.remove_food_by_id(food_id)

    def remove_food_by_id(self, food_id):
        if food_id in self.__food_dict.keys():
            food = self.__food_dict[food_id]
            self.remove_food(food)
            return True

        return False

    def remove_food(self, food):
        food_id = food.get_id()

        del self.__food_dict[food_id]

        food_y = food.get_y_position()
        food_x = food.get_x_position()

        self.__food_position_matrix[food_x][food_y] = None

        self.__food_count -= 1
        self.__food_available_positions.add((food_x, food_y))

    def remove_creature(self, creature):
        creature_id = creature.get_id()
        del self.__creatures_dict[creature_id]
        self.__position_matrix[creature.get_x()][creature.get_y()] = None
        self.__population -= 1
        self.__creatures_available_positions.add((creature.get_x(), creature.get_y()))

    def init_matrix(self):
        line = [0 for i in range(self.__screen.get_height())]
        line_food = [0 for i in range(self.__screen.get_height())]
        self.__position_matrix = [line for i in range(self.__screen.get_width())]
        self.__food_position_matrix = [line_food for i in range(self.__screen.get_width())]

    def count_cicles(self):
        self.__cicles += 1

    def create_creature(self, screen, velocity, sex=None, age=None, energy=None):

        if not len(self.__food_available_positions) > 0:
            return

        x, y = self.get_random_position()
        creature_id = self.get_id()

        while (x, y) not in self.__creatures_available_positions:
            x, y = self.get_random_position()

        if sex:
            new_creature = Creature(x, y, screen.get_width(),
                                    screen.get_height(), velocity, self.__creatures_size, creature_id, sex)
        else:
            creature_sex = None
            new_creature = Creature(x, y, screen.get_width(), screen.get_height(),
                                    velocity, self.__creatures_size, creature_id, creature_sex)

        if energy:
            new_creature.set_energy(energy)

        if age:
            new_creature.set_age(age)

        self.__save_creature(new_creature, x, y)

        if self.__render:
            self.__pg.draw.rect(self.__window, (0, 0, 255), (x, y, 10, 10))

        return new_creature

    def __save_creature(self, creature, x, y):
        creature_id = creature.get_id()
        self.__creatures_dict[creature_id] = creature
        self.__position_matrix[x][y] = creature_id
        self.__population += 1
        self.__all_time_population += 1
        self.__creatures_available_positions.remove((x, y))

    def create_food(self):

        # check if there is any available position
        if not len(self.__food_available_positions) > 0:
            return

        self.__food_count += 1

        x, y = self.get_random_position()

        while (x, y) not in self.__food_available_positions:
            x, y = self.get_random_position()

        self.__food_available_positions.remove((x, y))

        id = self.get_id()

        new_food = Food(x, y, id)

        self.__food_dict[id] = new_food
        self.__food_position_matrix[x][y] = id

        if self.__render:
            self.__pg.draw.rect(self.__window, (0, 255, 0), (x, y, 8, 8))

    def get_creature_matrix_id(self, x, y):
        return self.__position_matrix[x][y]

    def get_food_matrix_id(self, x, y):
        return self.__food_position_matrix[x][y]

    def get_creature_by_id(self, creature_id):
        return self.__creatures_dict[creature_id]

    def get_food_by_id(self, creature_id):
        return self.__food_dict[creature_id]
