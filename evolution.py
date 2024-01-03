import random
import importlib
from screen import Screen
from universe import Universe
from food import Food
from timeit import default_timer as timer
from stats_io import clear_file
from stats_io import append_csv_from_list
from creature import Creature
import json

import warnings

warnings.filterwarnings('ignore')  # setting ignore as a parameter


class Game(object):

    def __init__(self, pygame_object, numpy_object, pandas_object):

        self.__universe = None
        self.__window = None

        self.__pg = pygame_object
        self.__np = numpy_object
        self.__pd = pandas_object

        self.__consider_sex = False
        self.__food_wait = None
        self.__food_for_cicle = None
        self.__screen = None
        self.__initial_creatures = None
        self.__initial_food = None
        self.__max_food = None
        self.__cicle_size = None

        self.__display_simulation = True
        self.__print_stats = True
        self.__limit_population = False
        self.__population_limit = None
        self.__save_stats = True
        self.__stats_log = []

        self.__day_velocities_native = []
        self.__day_ages_native = []

        self.__load_configs()

        self.__population_record = 0
        self.__hungry_deaths = 0
        self.__age_deaths = 0
        self.__extinction = False

        self.__running_stats = None
        self.__day_velocities = None
        self.__day_ages = None
        self.__simulation_velocity = None

        self.__init_pygame(pygame_object)
        self.__init_stats(numpy_object, pandas_object)

        self.__cicle_time = 0
        self.__total_cicle_time = 0
        self.__creatures_born = 0

    def __init_stats(self, numpy_object, pandas_object):

        if self.__save_stats:
            clear_file('stats.csv')

        if numpy_object is None or pandas_object is None:
            self.__print_stats = False
            return

        self.__running_stats = self.__pd.DataFrame(columns=['velocity', 'day', 'age', 'population', 'food'])

        self.__day_velocities = self.__np.array([])
        self.__day_ages = self.__np.array([])
        self.__simulation_velocity = self.__np.array([])

    def __init_pygame(self, pygame_object):
        if pygame_object is not None:
            self.__display_simulation = True
            pygame.display.set_caption('Evolution Simulator')
            pygame.init()
            self.__window = self.__pg.display.set_mode((self.__screen.get_width(), self.__screen.get_height()))
            self.__universe = Universe(self.__window, 10, 10, self.__screen, self.__pg)

        else:
            self.__display_simulation = False
            self.__universe = Universe(None, 10, 10, self.__screen, self.__pg)

    def __load_configs(self):

        with open('config.json') as config_data:
            config_data = json.load(config_data)
            self.__cicle_size = config_data['cicleSize']
            self.__initial_food = config_data['initialFood']
            self.__initial_creatures = config_data['initialCreatures']
            self.__limit_population = config_data['limitPopulation']
            self.__max_food = config_data['maxFood']

            Creature.max_age = config_data['maxCreatureAge']
            Creature.max_energy = config_data['maxCreatureEnergy']
            Creature.reproduction_energy_cost = config_data['reproductionEnergyCost']
            Creature.food_energy = config_data['foodEnergy']
            Creature.reproduction_energy_minimum = config_data['reproductionEnergyMinimum']
            Creature.reproduction_age_start = config_data['reproductionAgeStart']
            Creature.reproduction_age_end = config_data['reproductionAgeEnd']
            Creature.mutation_range = config_data['mutationRange']
            Creature.min_velocity = config_data['minCreatureStartVelocity']
            Creature.max_velocity = config_data['maxCreatureStartVelocity']
            Creature.velocity_base_cost = config_data['velocityBaseCost']
            Creature.velocity_cost_rate = config_data['velocityCostRate']

            if self.__limit_population:
                self.__population_limit = config_data['populationLimit']

            else:
                self.__population_limit = float('inf')

            width = config_data['screenWidth']
            height = config_data['screenHeight']

            display_simulation = config_data['displaySimulation']
            if display_simulation:
                self.__screen = Screen(width, height, self.__pg)

            else:
                self.__screen = Screen(width, height, None)

            to_save_stats = config_data['saveStatsToFile']
            if to_save_stats:
                self.__save_stats = True

            else:
                self.__save_stats = False

            self.__food_wait = config_data['ciclesToSpawnFood']
            self.__food_for_cicle = config_data['foodForSpawn']
            Food.determined_duration = config_data['foodDuration']
            self.__consider_sex = config_data['considerTwoSexes']

    def __get_normal_distribution_random_number(self, min_value, max_value):
        return int((random.uniform(min_value, max_value) + random.uniform(min_value, max_value)) / 2)

    def get_cicle_size(self):
        return self.__cicle_size

    def get_born_creatures(self):
        return self.__creatures_born

    def get_simulation_velocity(self):
        return self.__simulation_velocity

    def get_all_time_population(self):
        return self.__population_record

    def get_hungry_deaths(self):
        return self.__hungry_deaths

    def get_age_deaths(self):
        return self.__age_deaths

    def get_extinction(self):
        return self.__extinction

    def get_cicles(self):
        return self.__universe.get_cicles()

    def get_population(self):
        return self.__universe.get_population()

    def get_food(self):
        return self.__universe.get_food()

    def get_population_record(self):
        return self.__population_record

    def get_population_limit(self):
        return self.__population_limit

    def get_universe(self):
        return self.__universe

    def get_stats(self):
        return self.__running_stats

    def get_random_position(self):
        x = random.randint(0, self.__screen.__width - 1)
        y = random.randint(0, self.__screen.get_height() - 1)
        return x, y

    def render_rood(self, food):
        rectangle = food.get_screen_rectangle()
        color = food.get_color_object()
        self.__screen.render_rectangle(self.__window, rectangle, color)

    def render_creature(self, creature):
        rectangle = creature.get_screen_rectangle()
        color = creature.get_color_object()
        self.__screen.render_rectangle(self.__window, rectangle, color)

    def start_world(self):

        min_velocity = Creature.min_velocity
        max_velocity = Creature.max_velocity
        max_energy = Creature.max_energy
        min_energy = int(max_energy / 5)

        print("creating food...")
        for i in range(self.__initial_food):
            self.__universe.create_food()

        print("creating creatures...")
        for i in range(self.__initial_creatures):

            velocity = self.__get_normal_distribution_random_number(min_velocity, max_velocity)
            energy = self.__get_normal_distribution_random_number(min_energy, max_energy)
            age = self.__get_normal_distribution_random_number(0, Creature.max_age)

            if self.__consider_sex:
                creature_sex = random.randint(0, 1)
                self.__universe.create_creature(self.__screen, velocity, sex=creature_sex, energy=energy, age=age)

            else:
                self.__universe.create_creature(self.__screen, velocity, energy=energy, age=age)

        print("population", self.__universe.get_population())
        print("food and creatures created, starting simulation..")
        self.__cicle_time = timer()

    def spawn_food(self):
        if self.__food_wait <= 0:
            for i in range(self.__food_for_cicle):
                self.__universe.create_food()
                if self.__universe.get_food_count() >= self.__max_food:
                    break
            self.__food_wait = 10
        self.__food_wait -= 1

    def ciclical_checks(self):
        self.spawn_food()
        self.counters()
        self.check_creatures()

        if self.__universe.get_population() > self.__population_record:
            self.__population_record = self.__universe.get_population()

        if self.__universe.get_population() == 0:
            self.__extinction = True

    def daily_checks(self):

        if self.__display_simulation:
            self.__window.fill((255, 255, 255))

        self.life_checks(render=self.__display_simulation)
        self.check_creatures(render=self.__display_simulation)

        if self.__display_simulation:
            self.__pg.display.update()

        self.compute_stats()
        self.evaluate_cicle_time()
        self.print_stats()
        self.clear_day_data()

    def trigger_stats_save(self):
        day = int(game.get_universe().get_cicles() / self.__cicle_size)
        if day % 1000 == 0:
            self.save_stats_to_file()

    def save_stats_to_file(self):
        if self.__save_stats:
            append_csv_from_list(self.__stats_log, 'stats.csv')
            del self.__stats_log[:]

    def compute_stats(self):
        day = int(game.get_universe().get_cicles() / self.__cicle_size)
        self.trigger_stats_save()
        if self.__print_stats:
            self.__running_stats = self.__pd.concat([self.__running_stats, self.__pd.DataFrame(
                {'age': [self.__day_ages.mean()],
                 'day': [day], 'velocity': [self.__day_velocities.mean()],
                 'population': [self.__universe.get_population()],
                 'food': [self.__universe.get_food_count()]
                 })])

        if self.__save_stats:
            average_age = sum(self.__day_ages_native) / len(self.__day_ages_native)
            average_velocity = sum(self.__day_velocities_native) / len(self.__day_velocities_native)
            self.__add_to_stats_logs(average_velocity, average_age, self.__universe.get_food_count())

    def clear_day_data(self):
        if not self.__print_stats:
            return
        self.__day_velocities = self.__np.array([])
        self.__day_ages = self.__np.array([])

        del self.__day_velocities_native[:]
        del self.__day_ages_native[:]

    def life_checks(self, render=True):
        self.check_food(render)
        self.check_creatures_lives()

    def check_creatures_lives(self):
        creatures = self.__universe.get_creature_dict().copy().items()
        for creature_id, creature in creatures:
            self.check_creature_life(creature)

    def check_food(self, render):
        food_list = self.__universe.get_food_dict().copy().items()
        for food_id, food in food_list:
            if render:
                self.render_rood(food)
            self.check_food_is_expired(food)

    def remove_creature(self, creature):
        self.__universe.remove_creature(creature)

    def counters(self):
        self.__food_wait -= 1
        self.__universe.count_cicles()

    def check_if_coordenates_inside_screen(self, x, y):
        if x >= self.__screen.get_width():
            return False
        elif y >= self.__screen.get_height():
            return False
        else:
            return True

    def check_creature_life(self, creature):
        # print("creature velocity: ", creature.velocity)
        alive = creature.is_alive()

        if self.__save_stats:
            self.__day_velocities_native.append(creature.get_velocity())
            self.__day_ages_native.append(int(creature.get_age() / self.__cicle_size))

        if self.__print_stats:
            self.__day_ages = self.__np.append(self.__day_ages, int(creature.get_age() / self.__cicle_size))
            self.__day_velocities = self.__np.append(self.__day_velocities, creature.get_velocity())

        if not alive:
            if creature.get_energy() <= 0:
                self.__hungry_deaths += 1
            else:
                self.__age_deaths += 1
            self.remove_creature(creature)

    def handle_creature_close_to_food(self, creature, x, y):
        removed = self.__universe.remove_food_by_position(x, y)
        if removed:
            creature.eat()
            return True

        return False

    def check_creature_proximity(self, creature):
        x = creature.get_x()
        y = creature.get_y()
        self.handle_creature_close_to_food(creature, x, y)
        self.check_reproduction(creature, x, y)

    def check_reproduction(self, creature, x, y):

        if self.__universe.get_population() >= self.__population_limit:
            return

        matrix_id = self.__universe.get_creature_matrix_id(x, y)
        if not creature.check_if_able_to_reproduce():
            return

        try:
            creature_to_reproduce = self.__universe.get_creature_by_id(matrix_id)
            if not creature_to_reproduce.check_if_able_to_reproduce():
                return

        except KeyError:
            return

        if self.__consider_sex:
            creature1_sex = creature.get_gender()
            creature2_sex = creature_to_reproduce.get_gender()
            if creature1_sex != creature2_sex:
                return

        new_velocity = creature.get_velocity() + creature_to_reproduce.get_velocity() / 2

        if self.__consider_sex:
            given_sex = random.randint(0, 1)
            if creature.get_gender() == 1:
                creature.reproduce()

            else:
                creature_to_reproduce.reproduce()

            self.__universe.create_creature(self.__screen, new_velocity, sex=given_sex)
            self.__creatures_born += 1
            return

        self.__creatures_born += 1
        creature.reproduce()
        self.__universe.create_creature(self.__screen, new_velocity)

    def check_food_is_expired(self, food):
        food.expire()
        expired = food.is_expired()
        if expired:
            self.__universe.remove_food(food)

    def __add_to_stats_logs(self, velocity, age, food):
        day = int(game.get_universe().get_cicles() / self.__cicle_size)
        line = str(day) + "," + str(int(velocity)) + "," \
               + str(age) + "," + str(self.get_population()) + "," + str(food) + "\n"
        self.__stats_log.append(line)

    def check_creatures(self, render=False):
        creatures = self.__universe.get_creature_dict().copy().items()
        for creature_id, creature in creatures:
            self.move_creature(creature, creature_id)

            if render:
                self.render_creature(creature)

    def move_creature(self, creature, creature_id):
        x = creature.get_x()
        y = creature.get_y()
        creature_velocity = creature.get_velocity()

        creature.before_move()
        for i in range(creature_velocity):
            self.__universe.remove_from_creatures_coordenates(x, y)
            x, y = creature.move()
            self.__universe.add_to_creatures_coordenates(x, y, creature_id)
            self.check_creature_proximity(creature)
        creature.after_move()

    def loop(self):
        if (game.__universe.get_cicles() % self.__cicle_size) == 0:
            self.daily_checks()

        self.ciclical_checks()

    def evaluate_cicle_time(self):
        self.__total_cicle_time = 0
        self.__total_cicle_time = timer() - self.__cicle_time
        self.__cicle_time = timer()

    def print_stats(self):
        objects = self.__universe.get_food_count() + self.__universe.get_population()
        velocity = (self.__total_cicle_time / objects) * 1000
        day = game.get_universe().get_cicles() / self.__cicle_size

        print("Population: ", self.__universe.get_population())
        print("Food: ", self.__universe.get_food_count())
        print("Age deaths: ", self.get_age_deaths())
        print("Starvation deaths: ", self.get_hungry_deaths())
        print("Creatures Born: ", self.__creatures_born)
        print("Day: %d" % day)

        print("Time taken to simulate day (s): %.5f" % self.__total_cicle_time)
        print("Velocity to simulate (s/obj): %.5f" % velocity)

        if self.__print_stats:
            average_creature_velocity = self.__running_stats.iloc[-1]['velocity']
            average_creature_age = self.__running_stats.iloc[-1]['age']
            self.__simulation_velocity = self.__np.append(self.__simulation_velocity, velocity)
            print("Average creature age: %d days" % average_creature_age)
            print("Average creature velocity: %d" % average_creature_velocity)


use_pygame = False
render_stats = False
pygame = None
numpy = None
pandas = None
stats = None
limit_execution = False
execution_limit = None

with open('config.json') as configs:
    data = json.load(configs)
    use_pygame = data['displaySimulation']
    limit_execution = data['limitExecutionInDays']
    execution_limit = data['daysLimit']
    render_stats = data['printStats']

if use_pygame:
    pygame = importlib.import_module('pygame')

if render_stats:
    numpy = importlib.import_module('numpy')
    pandas = importlib.import_module('pandas')
    stats = importlib.import_module('stats')

game = Game(pygame, numpy, pandas)
game.start_world()
run = True


def stop_execution(game_obj):
    if limit_execution:
        if game_obj.get_universe().get_cicles() > execution_limit * game_obj.get_cicle_size():
            return True
    if game_obj.get_extinction():
        return True
    return False


def print_summary(game_obj):
    print("\n===============SUMMARY===============")
    print("Population all times: ", game_obj.get_universe().get_all_time_population())
    print("Population record: ", game_obj.get_population_record())
    print("Simulated cicles: ", game_obj.get_universe().get_cicles())
    print("Starvation deaths: ", game_obj.get_hungry_deaths())
    print("Age deaths: ", game_obj.get_age_deaths())
    print("Final population: ", game_obj.get_universe().get_population())
    print("Born creatures: ", game_obj.get_born_creatures())
    print("Days simulated: %d" % (game_obj.get_universe().get_cicles() / game_obj.get_cicle_size()))

    if render_stats:
        simulation_average_velocity = numpy.average(game_obj.get_simulation_velocity())
        print("Average simulation velocity (s/obj): %.5f" % simulation_average_velocity)


def plot_history(game_obj):
    stats.plot_all_from_dataframe(game_obj.get_stats())


if use_pygame:
    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

        game.loop()
        if stop_execution(game):
            break
else:
    while run:
        game.loop()
        if stop_execution(game):
            break

run = False
game.save_stats_to_file()

if use_pygame:
    pygame.quit()

print_summary(game)

if render_stats:
    plot_history(game)
