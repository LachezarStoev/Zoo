from zoo import Zoo
from database import Database
from simulation import Simulation

def instructions():
    return '\n'.join(["see_animals",
        "accommodate <species> <age> <name> <gender> <weight>",
        "move_to_habitat <species> <name>",
        "simulate <interval_of_time> <period>",
        "exit"])

def main():
    db = Database("zoo.db")
    zoo = Zoo(50, 1000000000, db)
    simulation = Simulation(zoo)
    print("welcome to our zoo! enter help to get available commands")

    while True:
        commands = input("what'd you like to do? ").split(' ')
        command = commands[0]
        args = commands[1:]
        if command == 'help':
            print(instructions())
        elif command == 'simulate':
            try:
                simulation.simulate(*args)
            except AttributeError:
                print('\n'.join(["wrong command or wrong arguments entered!",
                    "maybe enter help again :)"]))
        elif command == 'exit':
            print('bye')
            exit(0)
        else:
            try:
                print(zoo.__getattribute__(command)(*args))
            except (TypeError, AttributeError):
                print('\n'.join(["wrong command or wrong arguments entered!",
                        "maybe enter help again :)"]))

    sm = Simulation(zoo)
    sm.simulation('months', 2)


if __name__ == '__main__':
    main()