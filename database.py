import sqlite3
from random import randint


class Database():

    def __init__(self, db_name="zoo.db"):
        self.name = db_name
        self.animal_conn = sqlite3.connect("animals.db")
        self.zoo_conn = sqlite3.connect(db_name)
        self.create_table()

    def create_table(self):
        c = self.zoo_conn.cursor()
        c.execute('''create table if not exists zoo
            (id integer primary key, name text,
                species text, age int, weight real, gender text)''')
        c.execute('''create table if not exists breeding
            (id int, last_breed int,
                foreign key (id) references zoo (id))''')

    def has_male(self, species):
        males = self.get_males(species)
        return len(males) > 0

    def get_male_name(self, species):
        males = self.get_males(species)
        rand_male = randint(0, len(males)-1)
        return males[rand_male][0]

    def get_males(self, species):
        c = self.zoo_conn.cursor()
        select_query = '''select name
                from zoo
                where gender='male' and species=?'''
        males = c.execute(select_query, (species, )).fetchall()
        return males

    def get_females(self):
        c = self.zoo_conn.cursor()
        females = c.execute('''select species, name
            from zoo where gender='female' ''').fetchall()
        return females

    def get_life_expectancy(self, species):
        c = self.animal_conn.cursor()
        life_expectancy = c.execute('''select life_expectancy
                from animals where species=?''',
            (species,)).fetchone()
        return life_expectancy[0]

    def get_food_type(self, species):
        c = self.animal_conn.cursor()
        food_type = c.execute('''select food_type
                from animals where species=?''',
            (species,)).fetchone()
        return food_type[0]

    def get_gestation(self, species):
        c = self.animal_conn.cursor()
        gestation = c.execute('''select gestation
                from animals where species=?''',
                (species,)).fetchone()
        return gestation[0]
        
    def get_newborn_weight(self, species):
        c = self.animal_conn.cursor()
        newborn_weight = c.execute('''select newborn_weight
                from animals where species=?''',
                (species,)).fetchone()
        return newborn_weight[0]

    def get_average_weight(self, species):
        c = self.animal_conn.cursor()
        weight = c.execute('''select average_weight
            from animals where species=?''', (species, )).fetchone()
        return weight[0]

    def get_weight_age_ratio(self, species):
        c = self.animal_conn.cursor()
        age = c.execute('''select weight_age_ratio from animals where species=?''',(species, )).fetchone()
        return age[0]

    def get_food_weight_ratio(self, species):
        c = self.animal_conn.cursor()
        food_weight_ratio = c.execute('''select food_weight_ratio
                from animals where species=?''',
            (species,)).fetchone()
        return food_weight_ratio[0]

    def insert_animal(self, animal):
        c = self.zoo_conn.cursor()
        c.execute('''insert into zoo(name, species, age, weight, gender)
            values(?, ?, ?, ?, ?)''',
            (animal.name, animal.species, animal.age,
            animal.weight, animal.gender))

        if animal.gender == "female":
            id = c.execute("select id from zoo").fetchall()
            id = id[-1][0]
            c.execute('''insert into breeding values(?, ?)''',
                (id, 0))
        self.zoo_conn.commit()

    def remove_animal(self, species, name):
        c = self.zoo_conn.cursor()
        animal_id = c.execute('''select id from zoo
                where species=? and name=?''',(species, name)).fetchone()
        if animal_id != None and len(animal_id) != 0:
            c.execute("delete from zoo where species=? and name=?",
                (species, name))
            c.execute("delete from breeding where id=?",
                (str(animal_id[0]),))
        self.zoo_conn.commit()  

    def set_last_breed(self, species, name, last_breed):
        c = self.zoo_conn.cursor()
        select_query = '''select id from zoo
            where species=? and name=?'''
        id_ = c.execute(select_query, (species, name)).fetchone()[0]
        update_query = '''update breeding
                set last_breed=?
                where id=?'''
        c.execute(update_query, (last_breed, id_))

    def get_last_breed(self, species, name):
        c = self.zoo_conn.cursor()
        last_breed = c.execute('''select last_breed
            from breeding
            join zoo
                on zoo.species=? and zoo.name=?
                and breeding.id=zoo.id''',
            (species, name)).fetchone()
        return last_breed[0]
