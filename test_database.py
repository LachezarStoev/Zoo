from database import Database
from animal import Animal
import unittest
from subprocess import call


class DatabaseTest(unittest.TestCase):
    def setUp(self):
        self.db = Database("test_zoo.db")
        self.a = Animal("lion", 24, "niya", "female", 150)
        self.db.insert_animal(self.a)
        self.c = self.db.zoo_conn.cursor()

    def test_database_init(self):
        self.assertEqual("test_zoo.db", self.db.name)

    def test_insert_animal(self):
        animal_from_db = self.c.execute('''select * from zoo''').fetchall()[0]
        self.assertEqual((1, "lion", 24, "niya", "female", 150),
                    animal_from_db)
        last_breed_from_db = self.c.execute('''select id, last_breed
                        from breeding''').fetchall()[0]
        self.assertEqual((1, 0), last_breed_from_db)

    def test_remove_animal(self):
        self.db.remove_animal("lion", "niya")

        animal_from_db = self.c.execute("select * from zoo").fetchall()
        self.assertEqual(0, len(animal_from_db))

        breed_from_db = self.c.execute("select * from breeding").fetchall()
        self.assertEqual(0, len(breed_from_db))

    def test_get_males_with_no_males(self):
        self.assertEqual(0, len(self.db.get_males("lion")))

    def test_get_males_with_one_male(self):
        a2 = Animal("lion", 24, "sharik", "male", 150)
        self.db.insert_animal(a2)
        self.assertEqual([("sharik", )], self.db.get_males("lion"))

    def test_has_male(self):
        self.assertFalse(self.db.has_male("lion"))

    def test_get_females(self):
        self.assertEqual([("lion", "niya")], self.db.get_females())

    def test_get_life_expectancy(self):
        self.assertEqual(15, self.db.get_life_expectancy("lion"))

    def test_get_food_type(self):
        self.assertEqual("carnivore", self.db.get_food_type("lion"))

    def test_get_gestation(self):
        self.assertEqual(3, self.db.get_gestation("lion"))

    def test_get_newborn_weight(self):
        self.assertEqual(2.0, self.db.get_newborn_weight("lion"))

    def test_get_average_weight(self):
        self.assertEqual(200, self.db.get_average_weight("lion"))

    def test_get_weight_age_ratio(self):
        self.assertEqual(7.5, self.db.get_weight_age_ratio("lion"))

    def test_get_food_weight_ration(self):
        self.assertEqual(0.035, self.db.get_food_weight_ratio("lion"))

    def test_get_last_breed(self):
        self.assertEqual(0, self.db.get_last_breed("lion", "niya"))

    def test_set_last_breed(self):
        self.db.set_last_breed("lion", "niya", 3)
        result = self.db.get_last_breed("lion", "niya")
        self.assertEqual(result, 3)

    def tearDown(self):
        call("rm {}".format(self.db.name), shell=True)


if __name__ == '__main__':
    unittest.main()