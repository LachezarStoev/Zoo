from zoo import Zoo


class Simulation():
    def __init__(self, zoo):
        self.zoo = zoo
        self.current_time = 0

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
        females = self.database.get_females()
        for i in range(iterations):
            for female in females:
                if self.zoo.will_it_mate(female[0], female[1]):
                    self.zoo.born_animal(female[0], female[1])
                    print("a new {} was born".format(female[0]))