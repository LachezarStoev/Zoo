import sqlite3


class DB():

	def __init__(self, db_name):
		self.name = db_name
		self.animal_conn = sqlite3.connect("animals.db")
		self.zoo_conn = sqlite3.connect(db_name)
		self.create_table()

	def create_table(self):
		c = self.zoo_conn
		c.execute(''' CREATE TABLE IF NOT EXISTS zoo
			(id INTEGER PRIMARY KEY, name text, species text, age int, weight real, gender text)''')
		c.execute(''' CREATE TABLE IF NOT EXISTS breed
			(animal_id int, last_breed int)''')

	def get_food_type(self, species):
		c = self.animal_conn.cursor()
		food_type = c.execute("SELECT food_type FROM animals WHERE species=?",(species,)).fetchone()
		return food_type[0]

	def insert_animal(self, animal):
		c = self.zoo_conn.cursor()
		c.execute("INSERT INTO zoo(name, species, age, weight, gender) VALUES(?,?,?,?,?)",(animal.name,animal.species,animal.age,animal.weight,animal.gender))
		if animal.gender == "female":
			id = c.execute("SELECT id FROM zoo").fetchall()
			id = id[len(id)-1][0]
			c.execute("INSERT INTO breed(animal_id, last_breed) VALUES(?,?)",(id,0)) #tyk nz kak se opredelq breed-a, moje bi 0 trqbva da e otnachalo
		self.zoo_conn.commit()

	def remove_animal(self, species, name):
		c = self.zoo_conn.cursor()
		id_of_animal = c.execute("SELECT id FROM zoo WHERE species=? and name=?",(species, name)).fetchone()
		if id_of_animal != []:
			c.execute("DELETE FROM zoo WHERE species=? and name=?",(species,name))
			c.execute("DELETE FROM breed WHERE animal_id=?",(str(id_of_animal[0]),))
		self.zoo_conn.commit()
	def get_last_breed(self, species, name):
		c = self.zoo_conn.cursor()
		id_of_animal = c.execute("SELECT id FROM zoo WHERE species=? and name=?",(species, name)).fetchone()
		last_breed = c.execute("SELECT last_breed FROM breed WHERE animal_id=?",(str(id_of_animal[0]))).fetchone()
		return last_breed[0]
