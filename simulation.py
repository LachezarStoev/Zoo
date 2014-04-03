from zoo import Zoo


class Simulation():
    def __init__(self, zoo):
        self.zoo = zoo
        self.current_time = 0
        self.interval_of_time = {}
        self.init_interval_of_time()

    def init_interval_of_time(self):
        self.interval_of_time["days"] = 1
        self.interval_of_time["weeks"] = 7
        self.interval_of_time["months"] = 30
        self.interval_of_time["years"] = 360

    def simulation(self, interval_of_time, period):
        interval = interval_of_time[:len(interval_of_time)-1]
        for i in range(period):
            print("-"*20)
            print("{} {}".format(interval, i+1))
            print("-"*20)
            self.simulate_cycle(interval_of_time)

    def alive_animals(self, interval_of_time):
        iterations = self.interval_of_time[interval_of_time] // 30
        for i in range(iterations):
            for animal in self.zoo.animals:
                if not animal.lives(self.zoo.database.get_life_expectancy(animal.species)):
                    self.zoo.remove(animal.species, animal.name)
                    print("{} the {} died".format(animal.name, animal.species))

    def get_money(self, interval_of_time):
        self.zoo.earn_budget(self.zoo.daily_incomes()\
            * self.interval_of_time[interval_of_time])

    def feed_animals(self, interval_of_time):
        amount = self.zoo.daily_incomes() * self.interval_of_time[interval_of_time]
        if self.zoo.budget >= amount:
            self.zoo.spend_budget(amount)
            return True
        else:
            return False

    def simulate_cycle(self, interval_of_time):
        self.grow_animals(interval_of_time)
        self.alive_animals(interval_of_time)
        self.feed_animals(interval_of_time)
        self.animals_to_be_born(interval_of_time)
        print(self.zoo.see_animals())

    def grow_animals(self, interval_of_time):
        self.days_to_pass = self.interval_of_time[interval_of_time]
        iterations = self.days_to_pass // 30 + self.current_time % 30
        for i in range(iterations):
            for animal in self.zoo.animals:
                average_weight =\
                    self.zoo.database.get_average_weight(animal.species)
                weight_age_ratio =\
                    self.zoo.database.get_weight_age_ratio(animal.species)
                animal.grow(average_weight, weight_age_ratio)

        return True

    def animals_to_be_born(self, interval_of_time):
        self.days_passed = self.interval_of_time[interval_of_time]
        iterations = self.days_passed // 30 + self.current_time % 30
        females = self.zoo.database.get_females()
        for i in range(iterations):
            for female in females:
                last_breed = self.zoo.database.get_last_breed(female[0], female[1])
                self.zoo.database.set_last_breed(female[0], female[1], last_breed + 1)
                if self.zoo.will_it_mate(female[0], female[1]):
                    self.zoo.born_animal(female[0], female[1])
                    self.zoo.database.set_last_breed(female[0], female[1], 0)
                    print("a new {} was born".format(female[0]))
