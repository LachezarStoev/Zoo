from database import DB
from animal import Animal
import unittest
from subprocess import call

class DataBaseTest(unittest.TestCase):
	def setUp(self):
		self.db=DB("testtable")
	def test_get_food_type(self):
		self.assertEqual("carnivore",self.db.get_food_type("lion"))
		self.assertEqual("herbivore",self.db.get_food_type("red panda"))
	def test_insert_animal(self):
		animal = Animal("lion", 24, "sharik", "male", 150)
		self.db.insert_animal(animal)

		c = self.db.zoo_conn.cursor()
		animal_from_db = c.execute("SELECT  name, species, age, weight, gender FROM zoo").fetchall()
		self.assertEqual(("sharik","lion",24,150,"male"),animal_from_db[0])

		animal_female = Animal("lion", 24, "Nia", "female", 150)
		self.db.insert_animal(animal_female)
		last_feed_from_db = c.execute("SELECT animal_id, last_breed FROM breed").fetchall()
		self.assertEqual((2,0),last_feed_from_db[0])

	def test_delete_animal(self):
		animal = Animal("lion", 24, "kirimitka", "female", 150)
		self.db.insert_animal(animal)
		self.db.remove_animal(animal.species,animal.name)

		c = self.db.zoo_conn.cursor()
		animal_from_db = c.execute("SELECT * FROM zoo").fetchall()
		self.assertEqual([],animal_from_db)

		breed_from_db = c.execute("SELECT * FROM breed").fetchall()
		self.assertEqual([],breed_from_db)
		
	def test_get_last_breed(self):
		animal = Animal("lion", 24, "Samanta", "female", 150)
		self.db.insert_animal(animal)
		last_breed = self.db.get_last_breed(animal.species, animal.name)
		self.assertEqual(0, last_breed)

	def tearDown(self):
		call("rm " + self.db.name,shell=True)

if __name__ == '__main__':
	unittest.main()