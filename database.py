import sqlite3


class Database():

	def __init__(self, db_name="zoo.db"):
		self.name = db_name
		self.animal_conn = sqlite3.connect("animals.db")
		self.zoo_conn = sqlite3.connect(db_name)
		self.create_table()

	def create_table(self):
		c = self.zoo_conn
		c.execute('''create table if not exists zoo
			(id integer primary key, name text,
                species text, age int, weight real, gender text)''')
		c.execute('''create table if not exists breeding
			(id int, last_breed int,
                foreign key (id) references zoo (id))''')

	def get_food_type(self, species):
		c = self.animal_conn.cursor()
		food_type = c.execute("select food_type from animals where species=?",
            (species,)).fetchone()
		return food_type[0]

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
		if len(animal_id) != 0:
			c.execute("delete from zoo where species=? and name=?",
                (species,name))
			c.execute("delete from breeding where id=?",
                (str(animal_id[0]),))
		self.zoo_conn.commit()  

	def get_last_breed(self, species, name):
		c = self.zoo_conn.cursor()
		last_breed = c.execute('''select last_breed
            from breeding
            join zoo
                on zoo.species=? and zoo.name=?
                and breeding.id=zoo.id''',
            (species, name)).fetchone()
		return last_breed[0]
