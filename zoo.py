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

    def spend_budget(self, amount):
        if self.budget >= amount:
            self.budget -= amount
            return True
        else:
            return False

    def earn_budget(self, amount):
        self.budget += amount

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

    def _random_gender(self):
        gender = randint(0, 1)
        if gender == 0:
            gender = "male"
        else:
            gender = "female"
        return gender

    def _generate_name(self, species, name, gender):
        male_name = self.database.get_male_name(species)
        if gender == 'male':
            return '{} {}'.format(male_name, name)
        else:
            return "{} {}".format(name, male_name)

    def born_animal(self, species, name):
        weight = self.database.get_newborn_weight(species)
        gender = self._random_gender()
        name = self._generate_name(species, name, gender)
        new_animal = animal.Animal(species, 1, name, gender, weight)
        self.animals.append(new_animal)
        self.database.insert_animal(new_animal)

    def will_it_mate(self, species, name):
        breeding_period =\
            Zoo.__BREEDING_PERIOD + self.database.get_gestation(species)
        has_mate = self.database.has_male(species)
        ready_to_breed =\
            breeding_period <= self.database.get_last_breed(species, name)

        return has_mate and ready_to_breed