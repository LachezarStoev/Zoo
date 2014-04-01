import animal
import database


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
            if animal_type == 'carnivore':
                cost += Zoo.__MEAT_COST * animal.feed()
            elif animal_type == 'herbivore':
                cost += Zoo.__GRASS_COST * animal.feed()

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
        new_animal= animal.Animal(species, name, gender, age, weight)
        self.animals.append(new_animal)
        self.database.insert_animal(animal.Animal(species, name, gender, age, weight))

        return True

    def move_to_habitat(self, species, name):
        self.capacity += 1

        for animal in self.animals:
            if animal.species == species and animal.name == name:
                self.animals.remove(animal)

        self.database.remove_animal(species, name)

    def will_it_mate(self, species, name):
        # TODO ready_to_mate = self.database.get_last_breed(species, name) == 0
        return ready_to_mate

    def simulation(self, interval_of_time, period):
        self.getattribute('_simulate_{0}'.format(interval_of_time))(period)

    def _simulate_days(self, period):
        for i in range(1, period + 1):
            print("day {}".format(i))


    def _simulate_weeks(self, period):
        pass
    def _simulate_months(self, period):
        pass
    def _simulate_years(self, period):
        pass