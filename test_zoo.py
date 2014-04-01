import unittest
from zoo import Zoo
from database import Database
from animal import Animal
from subprocess import call

class TestZoo(unittest.TestCase):
	def setUp(self):
		self.zoo = Zoo(5, 50, Database("test_zoo.db"))

	def test_init(self):
		self.assertEqual(5, self.zoo.capacity)
		self.assertEqual(50, self.zoo.budget)

	def test_accommodate(self):
		self.zoo.capacity = 0
		self.assertEqual(False,self.zoo.accommodate("lion", 24, "sharik", "male", 150))
		self.zoo.capacity = 5
		animal = Animal("lion", 24, "sharik", "male", 150)
		self.assertEqual(True,self.zoo.accommodate("lion", 24, "sharik", "male", 150))
		self.assertEqual(animal,self.zoo.animals[0])
		animals_from_db = self.zoo.database.zoo_conn.execute('''select * from zoo''').fetchall()
		self.assertEqual(1, len(animals_from_db))

<<<<<<< HEAD
	def test_move_to_habitat(self):
		self.zoo.accommodate("lion", 24, "sharik", "male", 150)
		self.zoo.move_to_habitat("lion", "sharik")
		self.assertEqual(0, len(self.zoo.animals))
		animals_from_db = self.zoo.database.zoo_conn.execute('''select * from zoo''').fetchall()
		self.assertEqual(0, len(animals_from_db))

	def test_daily_incomes(self):
		self.assertEqual(0,self.zoo.daily_incomes())

	def test_see_animals(self):
		self.zoo.accommodate("lion", 24, "sharik", "male", 150)
		expected = "sharik: lion, 24, 150"
		self.assertEqual(expected, self.zoo.see_animals())

	def test_daily_expenses(self):
		self.zoo.accommodate("lion", 24, "sharik", "male", 150)
		expected = 150 * self.zoo.database.get_food_ratio("lion")
		self.assertEqual(expected, self.zoo.daily_expenses())

	def tearDown(self):
		call("rm {}".format("test_zoo.db"),shell=True)

=======
>>>>>>> master
if __name__ == '__main__':
    unittest.main()
