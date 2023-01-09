import random
from color import Color
from screen_rectangle import ScreenRectangle


class Creature(object):
    max_energy = None
    max_age = None
    min_velocity = None
    max_velocity = None
    velocity_base_cost = None
    velocity_cost_rate = None
    reproduction_energy_cost = None
    reproduction_energy_minimum = None
    reproduction_age_start = None
    reproduction_age_end = None
    mutation_range = None
    food_energy = None

    def __init__(self, x, y, screen_x, screen_y, velocity, size, idnumber, gender):

        self.__x = x
        self.__y = y
        self.__screen_x = screen_x
        self.__screen_y = screen_y
        self.__velocity = velocity
        self.__life = Creature.max_age
        self.__age = 0
        self.__size = size
        self.__energy = Creature.max_energy
        self.__energy_max = Creature.max_energy
        self.__walking_direction = 0
        self.__idnumber = idnumber
        self.__alive = True
        self.__gender = gender
        self.__time_without_reproduction = 0
        self.__reproduction_wait = 1000
        self.__reproduction_age_start = 2000
        self.__reproduction_age_end = 7000
        self.__moving_functions = []

        self.reproduction_energy_cost = Creature.reproduction_energy_cost

        self.mutate()
        self.__init_moving_functions()

    def get_age(self):
        return self.__age

    def get_x(self):
        return self.__x

    def set_x(self, x):
        self.__x = x

    def set_y(self, y):
        self.__y = y

    def get_y(self):
        return self.__y

    def get_velocity(self):
        return self.__velocity

    def get_energy(self):
        return self.__energy

    def set_energy(self, energy):
        self.__energy = energy

    def set_age(self, age):
        self.__age = age

    def mutate(self):

        if self.__velocity < 0:
            self.__velocity = 0

        min_life = int(self.__life - self.__life * Creature.mutation_range)
        max_life = int(self.__life + self.__life * Creature.mutation_range)
        self.__life = int(random.randint(min_life, max_life))

        min_velocity = int(self.__velocity - self.__velocity * Creature.mutation_range)
        max_velocity = int(self.__velocity + self.__velocity * Creature.mutation_range)
        self.__velocity = int(random.randint(min_velocity, max_velocity))
        self.__velocity = int(self.__velocity)

        if self.__velocity < 0:
            self.__velocity = 0

    def __calculate_energy_expended_when_moving(self):
        cost = self.velocity_base_cost * self.__velocity
        return cost + (cost * self.velocity_cost_rate) ** 2

    def __init_moving_functions(self):
        self.__moving_functions.append(self.move_up)
        self.__moving_functions.append(self.move_down)
        self.__moving_functions.append(self.move_right)
        self.__moving_functions.append(self.move_left)
        self.__moving_functions.append(self.move_right_up)
        self.__moving_functions.append(self.move_right_down)
        self.__moving_functions.append(self.move_left_up)
        self.__moving_functions.append(self.move_left_down)

    def before_move(self):
        self.__use_energy(self.__calculate_energy_expended_when_moving())
        self.__walking_direction = random.randint(0, 7)

    def move(self):
        self.__moving_functions[self.__walking_direction]()
        return self.__x, self.__y

    def after_move(self):
        self.age()

    def get_color(self):
        color = int(2 * self.__original_velocity)
        if color > 255:
            color = 255

        if color < 0:
            color = 0

        return color

    def move_up(self):

        if self.__y + 1 < self.__screen_y:
            self.__y += 1
            return True

        return False

    def move_down(self):

        if self.__y - 1 > 0:
            self.__y -= 1
            return True

        return False

    def move_right(self):

        if self.__x + 1 < self.__screen_x:
            self.__x += 1
            return True

        return False

    def move_left(self):

        if self.__x - 1 > 0:
            self.__x -= 1
            return True

        return False

    def move_right_up(self):

        if self.__y + 1 < self.__screen_y and self.__x + 1 < self.__screen_x:
            self.__y += 1
            self.__x += 1
            return True

        return False

    def move_right_down(self):

        if self.__y - 1 > 0 and self.__x + 1 < self.__screen_x:
            self.__y -= 1
            self.__x += 1
            return True

        return False

    def move_left_up(self):

        if self.__y + 1 < self.__screen_y and self.__x - 1 > 0:
            self.__y += 1
            self.__x -= 1
            return True

        return False

    def move_left_down(self):

        if self.__y - 1 > 0 and self.__x - 1 > 0:
            self.__y -= 1
            self.__x -= 1
            return True

        return False

    def age(self):

        self.__age += 1

        if self.__age >= self.__life:
            self.__alive = False

    def __check_energy_expended(self):
        if self.__energy <= 0:
            self.__alive = False

    def __use_energy(self, quantity):
        self.__energy -= quantity
        self.__check_energy_expended()

    def is_alive(self):
        return self.__alive

    def get_id(self):
        return self.__idnumber

    def eat(self):
        self.__energy += 50
        if self.__energy > self.__energy_max:
            self.__energy = self.__energy_max

    def get_gender(self):
        return self.__gender

    def get_color_object(self):
        return Color(self.get_color(), 0, 255)

    def get_screen_rectangle(self):
        return ScreenRectangle(self.__x, self.__y, 10, 10)

    def reproduce(self):
        self.__time_without_reproduction = 0
        self.__use_energy(self.reproduction_energy_cost)
        self.__check_energy_expended()

    def check_if_able_to_reproduce(self):
        self.__time_without_reproduction += 1
        if self.__time_without_reproduction < self.__reproduction_wait:
            return False
        elif self.__energy < Creature.reproduction_energy_minimum:
            return False

        elif self.__age < Creature.reproduction_age_start:
            return False

        elif self.__age > Creature.reproduction_age_end:
            return False

        elif self.__time_without_reproduction < self.__reproduction_wait:
            return False

        return True
