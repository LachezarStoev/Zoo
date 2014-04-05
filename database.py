import sqlite3
from random import randint


class Database():
    def __init__(self, db_name="zoo.db"):
        self.name = db_name
        self.animals_conn = sqlite3.connect("animals.db")
        self.zoo_conn = sqlite3.connect(db_name)
        self.create_tables()

    def create_tables(self):
        c = self.zoo_conn.cursor()
        c.execute('''create table if not exists zoo
            (id integer primary key, species text, age int,
                name text, gender text, weight real)''')
        c.execute('''create table if not exists breeding
            (id int, last_breed int,
                foreign key (id) references zoo (id))''')
        self.zoo_conn.commit()

    def insert_animal(self, animal):
        c = self.zoo_conn.cursor()
        c.execute('''insert into zoo(species, age, name, gender, weight)
            values(?, ?, ?, ?, ?)''',
            (animal.species, animal.age, animal.name, 
            animal.gender, animal.weight))
        if animal.gender == "female":
            self._insert_into_breeding_table(animal)
        self.zoo_conn.commit()

    def _insert_into_breeding_table(self, animal):
        c = self.zoo_conn.cursor()
        id = c.execute("select id from zoo").fetchall()[-1]
        id = id[0]
        c.execute('''insert into breeding values(?, ?)''', (id, 0))
        self.zoo_conn.commit()

    def remove_animal(self, species, name):
        c = self.zoo_conn.cursor()
        animal_id = c.execute('''select id from zoo
                where species=? and name=?''',(species, name)).fetchone()
        if animal_id != None:
            c.execute("delete from zoo where species=? and name=?",
                (species, name))
            c.execute("delete from breeding where id=?",
                (str(animal_id[0]),))
        self.zoo_conn.commit()

    def update_animal(self, species, name, new_weight, new_age):
        c = self.zoo_conn.cursor()
        update_query = '''update zoo
                set weight=?, age=?
                where species=? and name=?'''
        c.execute(update_query, (new_weight, new_age,
            species, name))
        self.zoo_conn.commit()

    def get_males(self, species):
        c = self.zoo_conn.cursor()
        select_query = '''select name
                from zoo
                where gender='male' and species=?'''
        males = c.execute(select_query, (species, )).fetchall()
        return males

    def has_male(self, species):
        males = self.get_males(species)
        return len(males) > 0

    def get_male_name(self, species):
        males = self.get_males(species)
        rand_male = randint(0, len(males)-1)
        return males[rand_male][0]

    def get_females(self):
        c = self.zoo_conn.cursor()
        females = c.execute('''select species, name
            from zoo where gender='female' ''').fetchall()
        return females

    def _select_query(self, parameter, species):
        c = self.animals_conn.cursor()
        select_query = '''select {}
            from animals where species=?'''.format(parameter)
        result = c.execute(select_query, (species, )).fetchone()[0]
        return result

    def get_life_expectancy(self, species):
        return self._select_query('life_expectancy', species)

    def get_food_type(self, species):
        return self._select_query('food_type', species)

    def get_gestation(self, species):
        return self._select_query('gestation', species)
        
    def get_newborn_weight(self, species):
        return self._select_query('newborn_weight', species)

    def get_average_weight(self, species):
        return self._select_query('average_weight', species)

    def get_weight_age_ratio(self, species):
        return self._select_query('weight_age_ratio', species)

    def get_food_weight_ratio(self, species):
        return self._select_query('food_weight_ratio', species)

    def get_last_breed(self, species, name):
        c = self.zoo_conn.cursor()
        last_breed = c.execute('''select last_breed
                from breeding join zoo
                on zoo.species=? and zoo.name=?
                and breeding.id=zoo.id''',
            (species, name)).fetchone()[0]
        return last_breed

    def set_last_breed(self, species, name, last_breed):
        c = self.zoo_conn.cursor()
        select_query = '''select id from zoo
            where species=? and name=?'''
        id = c.execute(select_query, (species, name)).fetchone()[0]
        update_query = '''update breeding
                set last_breed=?
                where id=?'''
        c.execute(update_query, (last_breed, id))
        self.zoo_conn.commit()

    def get_animals(self):
        return self.zoo_conn.execute('''
            select species, age, name, gender, weight
            from zoo''')