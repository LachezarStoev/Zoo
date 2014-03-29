import sqlite3
class DB():
	def __init__(self, db_name):
		self.name = db_name
		self.animal_conn = sqlite3.connect("animals.db")
		self.zoo_conn = sqlite3.connect(db_name)
		self.create_table()
	def create_table(self):
		c = self.zoo_conn
		c.execute(''' CREATE TABLE IF NOT EXISTS {}
			(id INTEGER PRIMARY KEY, name text, species text, age int, weight real, gender text)'''.format(self.name))
		#c.execute(''' )
	def get_food_type(self, species):
		c = self.animal_conn.cursor()
		food_type = c.execute("SELECT food_type FROM animals WHERE species=?",(species,)).fetchall()
		return food_type[0][0]
	def insert_animal(self, animal):
		c = self.zoo_conn.cursor()
		c.execute("INSERT INTO "+self.name+"(name, species, age, weight, gender) VALUES(?,?,?,?,?)",(animal.name,animal.species,animal.age,animal.weight,animal.gender))
		#nito ? stava, nishto {}, nito %
		#ako namerish reshenie kaji
		self.zoo_conn.commit()
	def remove_animal(self, species, name):
		c = self.zoo_conn.cursor()
		c.execute("DELETE FROM "+self.name+" WHERE species=? and name=?",(species,name))
		self.zoo_conn.commit()