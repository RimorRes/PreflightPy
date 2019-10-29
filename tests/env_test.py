from .context import preflight as pre

class TestEnvUpdate:

    def test_pressure(self):
        parameters = pre.Parameters("tests/input/case.json")
        environment = pre.Environment(parameters.env_variables)
        environment.get_status(5000)
        assert round(environment.P, -1) == 54050
        environment.get_status(20000.0)
        assert round(environment.P, -1) == 5520
        with pytest.raises(Exception):
            assert environment.get_status(100000)

    def test_temperature(self):
        parameters = pre.Parameters("tests/input/case.json")
        environment = pre.Environment(parameters.env_variables)
        environment.get_status(5000)
        assert round(environment.T, 0) == 256
        environment.get_status(20000.0)
        assert round(environment.T, 0) == 217
        environment.get_status(40000.0)
        assert round(environment.T, 0) == 250

    def test_density(self):
        parameters = pre.Parameters("tests/input/case.json")
        environment = pre.Environment(parameters.env_variables)
        environment.get_status(5000)
        assert round(environment.Rho, 2) == 0.74
        environment.get_status(20000.0)
        assert round(environment.Rho, 2) == 0.09
        environment.get_status(40000.0)
        assert round(environment.Rho, 3) == 0.004


    def test_speed_of_sound(self):
        parameters = pre.Parameters("tests/input/case.json")
        environment = pre.Environment(parameters.env_variables)
        environment.get_status(1000)
        assert round(environment.c, 1) == 336.4
        environment.get_status(10000)
        assert round(environment.c, 1) == 299.5
        environment.get_status(30000)
        assert round(environment.c, 1) == 301.7
