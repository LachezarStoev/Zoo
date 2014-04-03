from zoo import Zoo


class Simulation():
    def __init__(self, zoo):
        self.zoo = zoo
        self.current_time = 0
        self.inverval_of_time = {}
        self.init_interval_of_time()

    def init_interval_of_time(self):
        self.interval_of_time["days"] = 1
        self.interval_of_time["weeks"] = 7
        self.interval_of_time["months"] = 30
        self.interval_of_time["years"] = 360

    def simulation(self, interval_of_time, period):
        for i in range(period):
            self.simulate_cycle(interval_of_time)

    def alive_animals(self, interval_of_time):
        iterations = self.inverval_of_time[interval_of_time] // 30
        for i in range(iterations):
            for animal in self.zoo.animals:
                if not animal.lives():
                    self.zoo.remove(animal.species, animal.name)
                    print("Animal with name: {} and species: {} died", animal.species, animal.name)

    def get_money(self, interval_of_time):
        return self.zoo.daily_incomes() * self.interval_of_time[interval_of_time]

    def feed_animals(self, interval_of_time):
        amount = self.zoo.daily_incomes() * self.interval_of_time[interval_of_time]
        if self.get_money(interval_of_time) >= amount:
            self.zoo.spend_budget(amount)
            return True
        else
            return False

    def simulate_cycle(self, interval_of_time):
        self.feed_animals(self, interval_of_time)
        self.grow_animals(interval_of_time)
        self.alive_animals(interval_of_time)
        self.animals_to_be_born(interval_of_time)




