import unittest
from main import BicycleRentalManager, App

class TestBicycleRentalManager(unittest.TestCase):
    def test_rent_bike_success(self):
        # This should succeed, because all the inputs are valid
        response = BicycleRentalManager.rent_bike(1, 2, "Covent Garden")
        self.assertEqual(response['status'], 'success')

        # This should succeed as well because nothing seems invalid
        response = BicycleRentalManager.rent_bike(10, 1, "Covent Garden")
        self.assertEqual(response['status'], 'success')

    def test_rent_bike_failure_invalid_id(self):
        # This should fail, because duration must be greater than 0
        response = BicycleRentalManager.rent_bike(12, -1, "Covent Garden")
        self.assertEqual(response['status'], 'failure')

        # This should fail, because we only have 50 bikes
        response = BicycleRentalManager.rent_bike(100, 200, "Covent Garden")
        self.assertEqual(response['status'], 'failure')


class TestApp(unittest.TestCase):
    def test_select_frame_by_name(self):
        app = App()
        app.select_frame_by_name("rent_bike_nav")
        self.assertTrue(app.winfo_ismapped())


if __name__ == '__main__':
    unittest.main()
