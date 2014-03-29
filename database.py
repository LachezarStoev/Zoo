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
			(id INTEGER PRIMARY KEY, name text, species text, age int, weight int)''')
		#c.execute(''' )
	def get_food_type(self, species):
		c=self.animal_conn.cursor()
		food_type = c.execute("SELECT food_type FROM animals WHERE species=?",(species,)).fetchall()
		return food_type[0][0]
