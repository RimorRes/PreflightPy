from .context import preflightpy as pre


class TestEnvUpdate:

    def test_pressure(self):
        environment = pre.Environment([
            113,
            0.01,
            9.80665,
            0.02896968,
            8.314462618,
            1.4,
            101325
            ])
        # Threshold set to ± 0.1%
        environment.get_status(0)
        assert abs(100 - round(environment.P, 0) / 101325 * 100) <= 0.1
        environment.get_status(5000)
        assert abs(100 - round(environment.P, -1) / 54040 * 100) <= 0.1
        environment.get_status(11019)
        assert abs(100 - round(environment.P, -1) / 22630 * 100) <= 0.1
        environment.get_status(20000)
        assert abs(100 - round(environment.P, -1) / 5530 * 100) <= 0.1
        environment.get_status(48000)
        assert abs(100 - round(environment.P, 0) / 102 * 100) <= 0.1
        environment.get_status(70000)
        assert abs(100 - round(environment.P, 1) / 5.2 * 100) <= 0.1
        environment.get_status(75000)
        assert abs(100 - round(environment.P, 1) / 2.4 * 100) <= 0.1
        environment.get_status(87000)
        assert abs(100 - round(environment.P, 2) / 0.31 * 100) <= 0.1
        environment.get_status(95000)
        assert abs(100 - round(environment.P, 3) / 0.076 * 100) <= 0.1
        environment.get_status(105000)
        assert abs(100 - round(environment.P, 3) / 0.014 * 100) <= 0.1
        environment.get_status(115000)
        assert abs(100 - round(environment.P, 4) / 0.0040 * 100) <= 0.1
        environment.get_status(140000)
        assert abs(100 - round(environment.P, 5) / 0.00072 * 100) <= 0.1
        environment.get_status(170000)
        assert abs(100 - round(environment.P, 5) / 0.00021 * 100) <= 0.1
        environment.get_status(250000)
        assert abs(100 - round(environment.P, 6) / 0.000025 * 100) <= 0.1
        environment.get_status(400000)
        assert abs(100 - round(environment.P, 8) / 1.45e-6 * 100) <= 0.1
        environment.get_status(625000)
        assert abs(100 - round(environment.P, 10) / 6.26e-8 * 100) <= 0.1
        environment.get_status(800000)
        assert abs(100 - round(environment.P, 10) / 1.70e-8 * 100) <= 0.1
        environment.get_status(1000000)
        assert abs(100 - round(environment.P, 11) / 7.51e-9 * 100) <= 0.1

    def test_temperature(self):
        environment = pre.Environment([
            113,
            0.01,
            9.80665,
            0.02896968,
            8.314462618,
            1.4,
            101325
            ])
        # Threshold set to ± 0.1%
        environment.get_status(5000)
        assert abs(100 - round(environment.T, 2) / 255.68 * 100) <= 0.1
        environment.get_status(20063)
        assert abs(100 - round(environment.T, 2) / 216.65 * 100) <= 0.1
        environment.get_status(30000)
        assert abs(100 - round(environment.T, 2) / 226.51 * 100) <= 0.1
        environment.get_status(47350)
        assert abs(100 - round(environment.T, 2) / 270.65 * 100) <= 0.1
        environment.get_status(71802)
        assert abs(100 - round(environment.T, 2) / 214.65 * 100) <= 0.1
        environment.get_status(87000)
        assert abs(100 - round(environment.T, 2) / 186.87 * 100) <= 0.1
        environment.get_status(100000)
        assert abs(100 - round(environment.T, 2) / 195.08 * 100) <= 0.1
        environment.get_status(115000)
        assert abs(100 - round(environment.T, 2) / 300.00 * 100) <= 0.1
        environment.get_status(125000)
        assert abs(100 - round(environment.T, 2) / 417.23 * 100) <= 0.1
        environment.get_status(160000)
        assert abs(100 - round(environment.T, 2) / 696.29 * 100) <= 0.1
        environment.get_status(330000)
        assert abs(100 - round(environment.T, 2) / 985.88 * 100) <= 0.1
        environment.get_status(500000)
        assert abs(100 - round(environment.T, 2) / 999.24 * 100) <= 0.1
        environment.get_status(750000)
        assert abs(100 - round(environment.T, 2) / 999.99 * 100) <= 0.1
        environment.get_status(1000000)
        assert abs(100 - round(environment.T, 2) / 1000.00 * 100) <= 0.1

    def test_density(self):
        environment = pre.Environment([
            113,
            0.01,
            9.80665,
            0.02896968,
            8.314462618,
            1.4,
            101325
            ])
        # Threshold set to ± 0.1%
        environment.get_status(0)
        assert abs(100 - round(environment.Rho, 4) / 1.2252 * 100) <= 0.1
        environment.get_status(5000)
        assert abs(100 - round(environment.Rho, 5) / 7.3643e-1 * 100) <= 0.1
        environment.get_status(11000)
        assert abs(100 - round(environment.Rho, 5) / 3.6480e-1 * 100) <= 0.1
        environment.get_status(20000)
        assert abs(100 - round(environment.Rho, 6) / 8.8910e-2 * 100) <= 0.1
        environment.get_status(70000)
        assert abs(100 - round(environment.Rho, 9) / 8.2829e-5 * 100) <= 0.1
        environment.get_status(87000)
        assert abs(100 - round(environment.Rho, 9) / 5.824e-6 * 100) <= 0.1
        environment.get_status(95000)
        assert abs(100 - round(environment.Rho, 9) / 1.393e-6 * 100) <= 0.1
        environment.get_status(105000)
        assert abs(100 - round(environment.Rho, 10) / 2.325e-7 * 100) <= 0.1
        environment.get_status(115000)
        assert abs(100 - round(environment.Rho, 11) / 4.289e-8 * 100) <= 0.1
        environment.get_status(140000)
        assert abs(100 - round(environment.Rho, 12) / 3.831e-9 * 100) <= 0.1
        environment.get_status(170000)
        assert abs(100 - round(environment.Rho, 13) / 7.815e-10 * 100) <= 0.1
        environment.get_status(250000)
        assert abs(100 - round(environment.Rho, 14) / 6.073e-11 * 100) <= 0.1
        environment.get_status(400000)
        assert abs(100 - round(environment.Rho, 15) / 2.803e-12 * 100) <= 0.1
        environment.get_status(625000)
        assert abs(100 - round(environment.Rho, 17) / 7.998e-14 * 100) <= 0.1
        environment.get_status(800000)
        assert abs(100 - round(environment.Rho, 17) / 1.136e-14 * 100) <= 0.1
        environment.get_status(1000000)
        assert abs(100 - round(environment.Rho, 18) / 3.561e-15 * 100) <= 0.1

    def test_speed_of_sound(self):
        environment = pre.Environment([
            113,
            0.01,
            9.80665,
            0.02896968,
            8.314462618,
            1.4,
            101325
            ])
        # Threshold set to ± 0.1%
        environment.get_status(1000)
        assert abs(100 - round(environment.c, 1) / 336.4 * 100) <= 0.1
        environment.get_status(10000)
        assert abs(100 - round(environment.c, 1) / 299.5 * 100) <= 0.1
        environment.get_status(30000)
        assert abs(100 - round(environment.c, 1) / 301.7 * 100) <= 0.1
