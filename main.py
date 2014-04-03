from zoo import Zoo
from database import Database
from simulation import Simulation


def main():
    db = Database("zoo.db")
    zoo = Zoo(100, 1000, db)

    zoo.accommodate("lion", 24, "sharik", "male", 150)
    zoo.accommodate("lion", 24, "simba", "male", 150)
    zoo.accommodate("lion", 24, "nala", "female", 130)
    zoo.accommodate("lion", 24, "nia", "female", 130)
    zoo.accommodate("lion", 24, "arya", "female", 130)
    zoo.accommodate("lion", 24, "nohra", "female", 130)

    sm = Simulation(zoo)
    sm.simulation('months', 6)
    




if __name__ == '__main__':
    main()