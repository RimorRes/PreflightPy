import preflightpy as pre


class TestParametersRetrieval:

    def test_params(self):
        parameters = pre.Parameters(engine=[303, 50000, 82],
                                    fuel=[0],
                                    mass=[1500],
                                    aero=[0.07, 0.255364],
                                    env=[110],
                                    sim=[0.01]
                                    )

        assert type(parameters.params) == dict
        assert parameters.params == {'engine': [303, 50000, 82],
                                     'fuel': [0],
                                     'mass': [1500],
                                     'aero': [0.07, 0.255364],
                                     'env': [110],
                                     'sim': [0.01]
                                     }

        parameters.params = [[303, 50000, 82],
                             [0],
                             [1500],
                             [0.07, 0.255364],
                             [110],
                             [0.01]
                             ]

        assert parameters.params == {'engine': [303, 50000, 82],
                                     'fuel': [0],
                                     'mass': [1500],
                                     'aero': [0.07, 0.255364],
                                     'env': [110],
                                     'sim': [0.01]
                                     }

    def test_properties(self):
        parameters = pre.Parameters()
        parameters.engine = [243, 500, 15]
        parameters.fuel = [0]
        parameters.mass = [10]
        parameters.aero = [0.0556, 0.0255364]
        parameters.env = [113]
        parameters.sim = [0.01]

        assert parameters.engine == [243, 500, 15]
        assert parameters.fuel == [0]
        assert parameters.mass == [10]
        assert parameters.aero == [0.0556, 0.0255364]
        assert parameters.env == [113]
        assert parameters.sim == [0.01]

    def test_repr(self):
        parameters = pre.Parameters()

        assert repr(parameters) == "simParametrs({'engine': None, 'fuel': None, 'mass': None, 'aero': None, 'env': None, 'sim': None})"  # noqa
