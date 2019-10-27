from context import preflight as pre
import unittest

class TestEnvUpdate(unittest.TestCase):

    def setUp(self):
        self.parameters = pre.Parameters("tests/input/case.json")
        self.environment = pre.Environment(self.parameters.env_variables)
        self.environment.get_status(3048)

    def test_pressure(self):
        self.assertEqual(round(self.environment.P, -3), 69000)

    def test_temperature(self):
        self.assertEqual(int(self.environment.T), 268)

    def test_density(self):
        self.assertEqual(round(self.environment.Rho, 1), 0.9)

    def test_speed_of_sound(self):
        self.assertEqual(int(self.environment.c), 328)

if __name__ == '__main__':
    unittest.main()
