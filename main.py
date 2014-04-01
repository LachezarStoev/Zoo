from zoo import Zoo
from database import Database


def main():
    db = Database("zoo.db")
    zoo = Zoo(100, 1000, db)

    zoo.accommodate("lion", 24, "sharik", "male", 150)
    zoo.accommodate("lion", 24, "nala", "female", 130)
    zoo.simulation('days', 3)



if __name__ == '__main__':
    main()