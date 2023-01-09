import random
from color import Color
from screen_rectangle import ScreenRectangle


class Creature(object):

    max_energy = None
    max_age = None
    min_velocity = None
    max_velocity = None
    velocityCostRate = None
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
        self.__original_velocity = velocity
        self.__velocity = 100 - velocity
        self.__life = Creature.max_age
        self.__age = 0
        self.__size = size
        self.__moving = False
        self.__steps = 0
        self.__walking_direction = 0
        self.__energy = Creature.max_energy
        self.__energy_max = Creature.max_energy
        self.__wait_to_velocity = ((100 - velocity) // 10)
        self.__idnumber = idnumber
        self.__alive = True
        self.__cicles = 0
        self.__gender = gender
        self.__time_without_reproduction = 0
        self.__reproduction_wait = 1000
        self.__reproduction_age_start = 2000
        self.__reproduction_age_end = 7000

        self.reproduction_energy_cost = Creature.reproduction_energy_cost

        self.mutate()

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
        self.__life += int(random.randint(min_life, max_life))

        min_velocity = int(self.__velocity - self.__velocity * Creature.mutation_range)
        max_velocity = int(self.__velocity + self.__velocity * Creature.mutation_range)
        self.__velocity += int(random.randint(min_velocity, max_velocity))

        if self.__velocity < 0:
            self.__velocity = 0

    def __calculate_energy_expended_when_moving(self):
        return (self.__velocity / 10) + (Creature.velocityCostRate * self.__velocity) ** 2

    def move(self):

        self.age_creature()
        self.__use_energy(self.__calculate_energy_expended_when_moving())
        self.__cicles += 1

        if self.__wait_to_velocity <= 0:

            moved = True

            if self.__steps == 0:

                self.__walking_direction = random.randint(1, 9)
                self.__steps = random.randint(10, 120)

            else:
                self.__steps -= 1

            if self.__walking_direction == 1:
                moved = self.move_up()

            if self.__walking_direction == 2:
                moved = self.move_down()

            if self.__walking_direction == 3:
                moved = self.move_right()

            if self.__walking_direction == 4:
                moved = self.move_left()

            if self.__walking_direction == 5:
                moved = self.move_right_up()

            if self.__walking_direction == 6:
                moved = self.move_right_down()

            if self.__walking_direction == 7:
                moved = self.move_left_up()

            if self.__walking_direction == 8:
                moved = self.move_left_down()

            if not moved:
                self.__steps = 0

            self.__wait_to_velocity = ((100 - self.__velocity) % 10)

        self.__wait_to_velocity -= 1
        return self.__x, self.__y

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

    def age_creature(self):

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
