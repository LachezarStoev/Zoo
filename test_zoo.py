import unittest
from zoo import Zoo
from database import Database
from animal import Animal
from subprocess import call


class TestZoo(unittest.TestCase):

    def setUp(self):
        self.zoo = Zoo(5, 50, Database("test_zoo.db"))
        self.a = ["lion", 24, "sharik", "male", 150]
        self.a2 = ["lion", 24, "niya", "female", 150]

    def test_zoo_init(self):
        self.assertEqual(5, self.zoo.capacity)
        self.assertEqual(50, self.zoo.budget)

    def test_accommodate(self):
        self.zoo.capacity = 0
        self.assertFalse(self.zoo.accommodate(*self.a))
        self.zoo.capacity = 5
        animal = Animal("lion", 24, "sharik", "male", 150)
        self.assertEqual(True, self.zoo.accommodate(*self.a))
        self.assertEqual(animal, self.zoo.animals[0])
        animals_from_db = self.zoo.database.zoo_conn.execute\
                ('''select * from zoo''').fetchall()
        self.assertEqual(1, len(animals_from_db))

    def test_move_to_habitat(self):
        self.zoo.accommodate(*self.a)
        self.zoo.move_to_habitat("lion", "sharik")
        self.assertEqual(0, len(self.zoo.animals))
        animals_from_db = self.zoo.database.zoo_conn.execute\
                ('''select * from zoo''').fetchall()
        self.assertEqual(0, len(animals_from_db))

    def test_see_animals(self):
        self.zoo.accommodate(*self.a)
        expected = "sharik the lion: 24 months, 150 kgs"
        self.assertEqual(expected, self.zoo.see_animals())

    def test_daily_incomes(self):
        self.assertEqual(0, self.zoo.daily_incomes())

    def test_daily_expenses(self):
        self.zoo.accommodate(*self.a)
        expected = 150 * 0.035
        self.assertEqual(expected * 4, self.zoo.daily_expenses())

    def test_spend_budget(self):
        result = self.zoo.spend_budget(50)
        self.assertEqual(0, self.zoo.budget)
        self.assertTrue(result)
        result = self.zoo.spend_budget(1)
        self.assertEqual(0, self.zoo.budget)
        self.assertFalse(result)

    def test_earn_budget(self):
        self.zoo.earn_budget(20)
        self.assertEqual(70, self.zoo.budget)

    def test_generate_name(self):
        self.zoo.accommodate(*self.a)
        male_name = self.zoo._generate_name("lion", "niya", "male")
        female_name = self.zoo._generate_name("lion", "niya", "female")
        self.assertEqual("sharik niya", male_name)
        self.assertEqual("niya sharik", female_name)

    def test_born_animal(self):
        self.zoo.accommodate(*self.a)
        self.zoo.accommodate(*self.a2)
        result = self.zoo.born_animal("lion", "niya")
        self.assertTrue(result)
        self.assertEqual(3, len(self.zoo.animals))

    def test_will_it_mate(self):
        self.zoo.accommodate(*self.a)
        self.zoo.accommodate(*self.a2)
        self.assertFalse(self.zoo.will_it_mate("lion", "niya"))
        self.zoo.database.set_last_breed("lion", "niya", 10)
        self.assertTrue(self.zoo.will_it_mate("lion", "niya"))

    def tearDown(self):
        call("rm -r {0}".format("test_zoo.db"), shell=True)

if __name__ == '__main__':
    unittest.main()
