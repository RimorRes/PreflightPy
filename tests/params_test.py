from .context import preflightpy as pre

class TestParametersRetrieval:

    def test_cast(self):
        c = lambda x: type(pre.Parameters.cast('', x))
        case = [
        8,
        19,
        603,
        1964,
        32415,
        367121,
        5664258,
        83948030,
        683032097,
        2144964292
        ]
        for i in case:
            assert c( i ) == float

        case = [
        1.624895098,
        65.52073166,
        218.1691716,
        6066.234004,
        10717.07395,
        812955.2693,
        5689667.860,
        10842368.66,
        542488750.2,
        3131879952.
        ]
        for i in case:
            assert c( i ) == float

        case = [
        "EREWvRW0NJ",
        "2QBP7NO2Cm",
        "J5603ng77j",
        "c0kbDuauJs",
        "82jBRk9Pm10",
        "o51QlnlcnL",
        "wrEdoJkkqa",
        "LFJtneD2NI",
        "vhK3urNqBT",
        "FcYrw4nQ7m"
        ]
        for i in case:
            assert c( i ) == str

        assert c( { 'a':1, 'b':2, 'c':3 } ) == str
        assert c( { 'a', 1, 'b', 2, 'c', 3 } ) == str

    def test_params_extension(self):
        p = pre.Parameters("tests/input/case.params")
        assert p.package == [ [318, 500], [15, 5], [10], [0.0556, 0.0255364], ["Flight.log", "Flight.csv"] ]
        assert p.env_variables == [113, 0.01, 9.80665, 0.02896968, 8.314462618, 1.4, 101325]

    def test_json_extension(self):
        p = pre.Parameters("tests/input/case.json")
        assert p.package == [ [318, 500], [15, 5], [10], [0.0556, 0.0255364], ["Flight.log", "Flight.csv"] ]
        assert p.env_variables == [113, 0.01, 9.80665, 0.02896968, 8.314462618, 1.4, 101325]
