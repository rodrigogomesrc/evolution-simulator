import random
import importlib
from screen import Screen
from universe import Universe
from food import Food
from timeit import default_timer as timer
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
        self.__screen = None
        self.__initial_creatures = None
        self.__initial_food = None
        self.__cicle_size = None

        self.__display_simulation = True
        self.__print_stats = True
        self.__limit_population = False
        self.__population_limit = None

        self.__load_configs()

        self.__population_record = 0
        self.__hungry_deaths = 0
        self.__age_deaths = 0
        self.__extinction = False

        self.__average_velocity = None
        self.__average_age = None
        self.__day_velocities = None
        self.__day_ages = None
        self.__simulation_velocity = None

        self.__init_pygame(pygame_object)
        self.__init_stats(numpy_object, pandas_object)

        self.__cicle_time = 0
        self.__total_cicle_time = 0



    def __init_stats(self, numpy_object, pandas_object):

        if numpy_object is None or pandas_object is None:
            self.__print_stats = False
            return

        self.__average_velocity = self.__pd.DataFrame(columns=['velocity', 'day'])
        self.__average_age = self.__pd.DataFrame(columns=['age', 'day'])
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

            self.__food_wait = config_data['ciclesToSpawnFood']
            Food.determined_duration = config_data['foodDuration']
            self.__consider_sex = config_data['considerTwoSexes']

    def get_cicle_size(self):
        return self.__cicle_size

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

    def get_simulation_velocity(self):
        return self.__simulation_velocity

    def get_average_velocity(self):
        return self.__average_velocity

    def get_average_age(self):
        return self.__average_age

    def get_population_limit(self):
        return self.__population_limit

    def get_universe(self):
        return self.__universe

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

        print("creating food...")
        for i in range(self.__initial_food):
            self.__universe.create_food()

        print("creating creatures...")
        for i in range(self.__initial_creatures):
            velocity = random.randint(30, 100)
            if self.__consider_sex:
                creature_sex = random.randint(0, 1)
                self.__universe.create_creature(self.__screen, velocity, sex=creature_sex)

            else:
                self.__universe.create_creature(self.__screen, velocity)

        print("food and creatures created, starting simulation..")
        self.__cicle_time = timer()

    def spawn_food(self):
        if self.__food_wait <= 0:
            self.__universe.create_food()
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

    def compute_stats(self):
        if not self.__print_stats:
            return
        day = int(game.get_universe().get_cicles() / self.__cicle_size)
        self.__average_velocity = self.__pd.concat([self.__average_velocity, self.__pd.DataFrame(
            {'velocity': [self.__day_velocities.mean()], 'day': [day]})])

        self.__average_age = self.__pd.concat([self.__average_age, self.__pd.DataFrame(
            {'age': [self.__day_ages.mean()], 'day': [day]})])

    def clear_day_data(self):
        if not self.__print_stats:
            return
        self.__day_velocities = self.__np.array([])
        self.__day_ages = self.__np.array([])

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

        if self.__universe.get_population() >= self.__population_limit:
            return

        matrix_id = self.__universe.get_creature_matrix_id(x, y)
        if not creature.check_if_able_to_reproduce():
            return

        # TODO: logic considering sex
        if self.__consider_sex:
            return

        try:
            creature_to_reproduce = self.__universe.get_creature_by_id(matrix_id)

        except KeyError:
            return

        new_velocity = creature.get_velocity() + creature_to_reproduce.get_velocity() / 2
        self.__universe.create_creature(self.__screen, new_velocity)

    def check_food_is_expired(self, food):
        food.expire()
        expired = food.is_expired()
        if expired:
            self.__universe.remove_food(food)

    def check_creatures(self, render=False):
        creatures = self.__universe.get_creature_dict().copy().items()
        for creature_id, creature in creatures:
            self.move_creature(creature, creature_id)
            self.check_creature_proximity(creature)

            if render:
                self.render_creature(creature)

    def move_creature(self, creature, creature_id):
        x = creature.get_x()
        y = creature.get_y()
        self.__universe.remove_from_creatures_coordenates(x, y)
        x, y = creature.move()
        self.__universe.add_to_creatures_coordenates(x, y, creature_id)

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
        print("Day: %d" % day)

        print("Time taken to simulate day (s): %.5f" % self.__total_cicle_time)
        print("Velocity to simulate (s/obj): %.5f" % velocity)

        if self.__print_stats:
            average_creature_velocity = self.__average_velocity.iloc[-1]['velocity']
            average_creature_age = self.__average_age.iloc[-1]['age']
            self.__simulation_velocity = self.__np.append(self.__simulation_velocity, velocity)
            print("Average creature age: %d days" % average_creature_age)
            print("Average creature velocity: %d" % average_creature_velocity)


use_pygame = True
render_stats = True
pygame = None
numpy = None
pandas = None
plt = None
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
    plt = importlib.import_module('matplotlib.pyplot')

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
    print("Cicles simulated: ", game_obj.get_universe().get_cicles())
    print("Hungry deaths: ", game_obj.get_hungry_deaths())
    print("age_deaths: ", game_obj.get_hungry_deaths())
    print("Days simulated: %d" % (game_obj.get_universe().get_cicles() / game_obj.get_cicle_size()))

    if render_stats:
        simulation_average_velocity = numpy.average(game_obj.get_simulation_velocity())
        print("Average simulation velocity (s/obj): %.5f" % simulation_average_velocity)


def plot_history(game_obj):
    plt.plot(game_obj.get_average_velocity()['day'], game_obj.get_average_velocity()['velocity'],
             label='Average velocity')
    plt.plot(game_obj.get_average_age()['day'], game_obj.get_average_age()['age'], label='Average age')
    plt.title('Average velocity and age by day')
    plt.xlabel('Day')
    plt.ylabel('Average velocity and age')
    plt.legend()
    plt.show()


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
if use_pygame:
    pygame.quit()

print_summary(game)

if render_stats:
    plot_history(game)
