from zoo import Zoo


class Simulation():
    def __init__(self, zoo):
        self.zoo = zoo
        self.current_time = 0
        self.interval_of_time = {}
        self._init_interval_of_time()
        self._new_animals_hash = {}

    def _init_interval_of_time(self):
        self.interval_of_time["days"] = 1
        self.interval_of_time["weeks"] = 7
        self.interval_of_time["months"] = 30
        self.interval_of_time["years"] = 360

    def simulate(self, interval_of_time, period):
        period = int(period)
        interval = interval_of_time[:-1]
        for i in range(period):
            print("-"*20)
            print("{} {}".format(interval, i+1))
            print("-"*20)
            self.simulate_cycle(interval_of_time)
            self.current_time += self.interval_of_time[interval_of_time]

    def simulate_cycle(self, interval_of_time):
        self.grow_animals(interval_of_time)
        self.alive_animals(interval_of_time)
        self.feed_animals(interval_of_time)
        self.get_money(interval_of_time)
        self.animals_to_be_born(interval_of_time)
        print(self.zoo.see_animals())

    def _calculate_iterations(self, interval_of_time):
        days_from_last_month = self.current_time % 30
        days_to_pass = self.interval_of_time[interval_of_time]
        iterations = (days_to_pass + days_from_last_month) // 30
        return iterations

    def _grow_information(self, species):
        average_weight =\
            self.zoo.database.get_average_weight(species)
        weight_age_ratio =\
            self.zoo.database.get_weight_age_ratio(species)
        return average_weight, weight_age_ratio


    def grow_animals(self, interval_of_time):
        iterations = self._calculate_iterations(interval_of_time)
        for i in range(iterations):
            for animal in self.zoo.animals:
                animal.grow(*self._grow_information(animal.species))
                self.zoo.database.update_animal(animal.species, animal.name,
                    animal.weight, animal.age)
        return True

    def _remove_dead_animals(self):
        for animal in self.zoo.animals:
            if not animal.lives(\
                    self.zoo.database.get_life_expectancy(animal.species)):
                self.zoo.remove(animal.species, animal.name)
                print("{} the {} died".format(animal.name, animal.species))
                if (animal.species, animal.name) in self._new_animals_hash:
                    del self._new_animals_hash[animal.species, animal.name]

    def alive_animals(self, interval_of_time):
        iterations = self._calculate_iterations(interval_of_time)
        for i in range(iterations):
            self._remove_dead_animals()

    def feed_animals(self, interval_of_time):
        amount = self.zoo.daily_incomes() *\
                self.interval_of_time[interval_of_time]
        if self.zoo.budget >= amount:
            self.zoo.spend_budget(amount)
        else:
            print(' '.join(["the zoo doesn't have enough budget",
                "to feed all animals!"]))
            exit(1)

    def get_money(self, interval_of_time):
        self.zoo.earn_budget(self.zoo.daily_incomes() *\
                self.interval_of_time[interval_of_time])

    def _add_to_new_animals_hash(self, female_animal):
        self._new_animals_hash[female_animal] = (female_animal, 0)

    def _update_new_animals_hash(self):
        to_remove = []
        for female_animal in self._new_animals_hash.items():
            value = female_animal[1]
            key = female_animal[0]
            species = value[0][0]
            if value[1] >=\
                    self.zoo.database.get_gestation(species):
                self.zoo.born_animal(*value[0])
                print("a new {} was born".format(species))
                to_remove.append(key)
            else:
                self._new_animals_hash[key] =\
                    (value[0], value[1] + 1)

        for animal in to_remove:
            del self._new_animals_hash[animal]

    def _will_be_there_a_new_animal(self, female_animal):
        last_breed = self.zoo.database.get_last_breed(*female_animal)
        self.zoo.database.set_last_breed(\
            female_animal[0], female_animal[1], last_breed + 1)
        if self.zoo.will_it_mate(*female_animal):
            self._add_to_new_animals_hash(female_animal)
            self.zoo.database.set_last_breed(\
                female_animal[0], female_animal[1], 0)
        self._update_new_animals_hash()

    def animals_to_be_born(self, interval_of_time):
        iterations = self._calculate_iterations(interval_of_time)
        females = self.zoo.database.get_females()
        for i in range(iterations):
            for female_animal in females:
                self._will_be_there_a_new_animal(female_animal)
