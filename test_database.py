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
		animal_from_db = c.execute("SELECT  name, species, age, weight, gender FROM {}".format(self.db.name)).fetchall()
		self.assertEqual(("sharik","lion",24,150,"male"),animal_from_db[0])

	def tearDown(self):
		call("rm " + self.db.name,shell=True)

if __name__ == '__main__':
	unittest.main()