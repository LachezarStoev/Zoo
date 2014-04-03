import animal
import database
from random import randint


class Zoo():

    __INCOME_PER_ANIMAL = 60
    __MEAT_COST = 4
    __GRASS_COST = 2
    __BREEDING_PERIOD = 6

    def __init__(self, capacity, budget, database):
        self.capacity = capacity
        self.budget = budget
        self.database = database
        self.animals = []

    def daily_incomes(self):
        return Zoo.__INCOME_PER_ANIMAL * len(self.animals)

    def daily_expenses(self):

        cost = 0
        for animal in self.animals:
            animal_type = self.database.get_food_type(animal.species)
            food_weight_ratio =\
                self.database.get_food_weight_ratio(animal.species)
            if animal_type == 'carnivore':
                cost += Zoo.__MEAT_COST * animal.feed(food_weight_ratio)
            elif animal_type == 'herbivore':
                cost += Zoo.__GRASS_COST * animal.feed(food_weight_ratio)

        return cost

    def see_animals(self):
        animal_list = []

        for animal in self.animals:
            animal_list.append(str(animal))

        return '\n'.join(animal_list)

    def random_gender(self):
        gender = randint(0, 1)
        if gender == 0:
            gender = "male"
        else:
            gender = "female"
        return gender

    def _animal_is_born(self, father, mother):
        gender = self.random_gender()

    def accommodate(self, species, name, gender, age, weight):
        if self.capacity <= 0:
            return False

        self.capacity -= 1
        new_animal = animal.Animal(species, name, gender, age, weight)
        self.animals.append(new_animal)
        self.database.insert_animal(animal.Animal(species,
                name, gender, age, weight))

        return True

    def remove(self, species, name):
        self.capacity += 1

        for animal in self.animals:
            if animal.species == species and animal.name == name:
                self.animals.remove(animal)

        self.database.remove_animal(species, name)

    def move_to_habitat(self, species, name):
        remove(species, name)

    def will_it_mate(self, species, name):
        breeding_period =\
            Zoo.__BREEDING_PERIOD + self.database.get_gestation(species)
        ready_to_mate =\
            breeding_period <= self.database.get_last_breed(species, name)
        return ready_to_mate

    def simulation(self, interval_of_time, period):
        for i in range(period):
            print("\n{0} {1}:".format(interval_of_time, i + 1))
            self.__getattribute__\
                ('_simulate_{0}'.format(interval_of_time))(period)

    def _simulate_days(self, period):
        for animal in self.animals:
            if not animal.lives\
                    (self.database.get_life_expectancy(animal.species)):
                self.animals.remove(animal)
                self.database.remove_animal(animal.species, animal.name)
                died = "{} {} has died..".format(animal.name, animal.species)
                print(died)
            elif animal.gender == "female" and self.database.ready_to_mate():

        expenses = "daily expenses: {}".format(self.daily_expenses())
        print(expenses)
        print(self.see_animals())



    def _simulate_weeks(self, period):
        pass
    def _simulate_months(self, period):
        pass
    def _simulate_years(self, period):
        pass