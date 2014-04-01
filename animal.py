from random import randint


class Animal():
    def __init__(self, species, age, name, gender, weight):
        self.species = species
        self.age = age
        self.name = name
        self.gender = gender
        self.weight = weight
        
    def __eq__(self, other):
        return self.name == other.name and self.species == other.species

    def __str__(self):
        return "{0}: {1}, {2}, {3}".format(self.name,
                    self.species, self.age, self.weight)

    def grow(self, average_weight, weight_age_ratio):
        if self.weight < average_weight:
            self.weight += weight_age_ratio 
        self.age += 1

    def lives(self, life_expectancy):
        life_expectancy_in_months = life_expectancy * 12
        return randint(1, life_expectancy_in_months) > self.age
        
    def feed(self, food_weight_ratio):
        return food_weight_ratio * self.weight