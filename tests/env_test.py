from .context import preflight as pre

class TestEnvUpdate:

    def test_pressure(self):
        parameters = pre.Parameters("tests/input/case.json")
        environment = pre.Environment(parameters.env_variables)
        environment.get_status(3048)
        assert round(environment.P, -3) == 69000

    def test_temperature(self):
        parameters = pre.Parameters("tests/input/case.json")
        environment = pre.Environment(parameters.env_variables)
        environment.get_status(3048)
        assert int(environment.T) == 268

    def test_density(self):
        parameters = pre.Parameters("tests/input/case.json")
        environment = pre.Environment(parameters.env_variables)
        environment.get_status(3048)
        assert round(environment.Rho, 1) == 0.9

    """def test_speed_of_sound(self):
        parameters = pre.Parameters("tests/input/case.json")
        environment = pre.Environment(parameters.env_variables)
        environment.get_status(3048)
        assert int(environment.c) == 328"""
