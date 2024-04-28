import unittest
from main import BicycleRentalSystem

#####
# in the following, we will write some test cases
# for testing the logic handler methods of our
# app using the `unittest` python standard library
#####
class TestBicycleRentalSystem(unittest.TestCase):
    def setUp(self):
        self.brs = BicycleRentalSystem()

    def test_rent_bicycle_valid(self):
        result = self.brs.rent_bicycle(1, 2, "South Bank Riverside")
        self.assertEqual(result['status'], 'ok')

    def test_rent_bicycle_invalid_id(self):
        result = self.brs.rent_bicycle(200, 2, "South Bank Riverside")
        self.assertEqual(result['status'], 'failure')

    def test_rent_bicycle_invalid_duration(self):
        result = self.brs.rent_bicycle(1, "abc", "South Bank Riverside")
        self.assertEqual(result['status'], 'failure')

    def test_rent_bicycle_missing_inputs(self):
        result = self.brs.rent_bicycle(None, None, None)
        self.assertEqual(result['status'], 'failure')

    def test_return_bicycle_valid(self):
        self.brs.rent_bicycle(1, 2, "South Bank Riverside")
        result = self.brs.return_bicycle(1, 3)
        self.assertEqual(result['status'], 'ok')

    def test_return_bicycle_invalid_id(self):
        result = self.brs.return_bicycle(200, 2)
        self.assertEqual(result['status'], 'failure')

    def test_return_bicycle_not_rented(self):
        result = self.brs.return_bicycle(1, 2)
        self.assertEqual(result['status'], 'failure')

    def test_return_bicycle_invalid_duration(self):
        result = self.brs.return_bicycle(1, "abc")
        self.assertEqual(result['status'], 'failure')


if __name__ == '__main__':
    unittest.main()
