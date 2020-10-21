import preflightpy as pre


class TestEnvUpdate:

    def test_pressure(self):
        env = pre.get_env_variables
        # Threshold set to ± 0.1%
        g, temp, pressure, density, c = env(0)
        assert abs(100 - round(pressure, 0) / 101325 * 100) <= 0.1
        g, temp, pressure, density, c = env(5000)
        assert abs(100 - round(pressure, -1) / 54040 * 100) <= 0.1
        g, temp, pressure, density, c = env(11019)
        assert abs(100 - round(pressure, -1) / 22630 * 100) <= 0.1
        g, temp, pressure, density, c = env(20000)
        assert abs(100 - round(pressure, -1) / 5530 * 100) <= 0.1
        g, temp, pressure, density, c = env(48000)
        assert abs(100 - round(pressure, 0) / 102 * 100) <= 0.1
        g, temp, pressure, density, c = env(70000)
        assert abs(100 - round(pressure, 1) / 5.2 * 100) <= 0.1
        g, temp, pressure, density, c = env(75000)
        assert abs(100 - round(pressure, 1) / 2.4 * 100) <= 0.1
        g, temp, pressure, density, c = env(87000)
        assert abs(100 - round(pressure, 2) / 0.31 * 100) <= 0.1
        g, temp, pressure, density, c = env(95000)
        assert abs(100 - round(pressure, 3) / 0.076 * 100) <= 0.1
        g, temp, pressure, density, c = env(105000)
        assert abs(100 - round(pressure, 3) / 0.014 * 100) <= 0.1
        g, temp, pressure, density, c = env(115000)
        assert abs(100 - round(pressure, 4) / 0.0040 * 100) <= 0.1
        g, temp, pressure, density, c = env(140000)
        assert abs(100 - round(pressure, 5) / 0.00072 * 100) <= 0.1
        g, temp, pressure, density, c = env(170000)
        assert abs(100 - round(pressure, 5) / 0.00021 * 100) <= 0.1
        g, temp, pressure, density, c = env(250000)
        assert abs(100 - round(pressure, 6) / 0.000025 * 100) <= 0.1
        g, temp, pressure, density, c = env(400000)
        assert abs(100 - round(pressure, 8) / 1.45e-6 * 100) <= 0.1
        g, temp, pressure, density, c = env(625000)
        assert abs(100 - round(pressure, 10) / 6.26e-8 * 100) <= 0.1
        g, temp, pressure, density, c = env(800000)
        assert abs(100 - round(pressure, 10) / 1.70e-8 * 100) <= 0.1
        g, temp, pressure, density, c = env(1000000)
        assert abs(100 - round(pressure, 11) / 7.51e-9 * 100) <= 0.1

    def test_temperature(self):
        env = pre.get_env_variables
        # Threshold set to ± 0.1%
        g, temp, pressure, density, c = env(5000)
        assert abs(100 - round(temp, 2) / 255.68 * 100) <= 0.1
        g, temp, pressure, density, c = env(20063)
        assert abs(100 - round(temp, 2) / 216.65 * 100) <= 0.1
        g, temp, pressure, density, c = env(30000)
        assert abs(100 - round(temp, 2) / 226.51 * 100) <= 0.1
        g, temp, pressure, density, c = env(47350)
        assert abs(100 - round(temp, 2) / 270.65 * 100) <= 0.1
        g, temp, pressure, density, c = env(71802)
        assert abs(100 - round(temp, 2) / 214.65 * 100) <= 0.1
        g, temp, pressure, density, c = env(87000)
        assert abs(100 - round(temp, 2) / 186.87 * 100) <= 0.1
        g, temp, pressure, density, c = env(100000)
        assert abs(100 - round(temp, 2) / 195.08 * 100) <= 0.1
        g, temp, pressure, density, c = env(115000)
        assert abs(100 - round(temp, 2) / 300.00 * 100) <= 0.1
        g, temp, pressure, density, c = env(125000)
        assert abs(100 - round(temp, 2) / 417.23 * 100) <= 0.1
        g, temp, pressure, density, c = env(160000)
        assert abs(100 - round(temp, 2) / 696.29 * 100) <= 0.1
        g, temp, pressure, density, c = env(330000)
        assert abs(100 - round(temp, 2) / 985.88 * 100) <= 0.1
        g, temp, pressure, density, c = env(500000)
        assert abs(100 - round(temp, 2) / 999.24 * 100) <= 0.1
        g, temp, pressure, density, c = env(750000)
        assert abs(100 - round(temp, 2) / 999.99 * 100) <= 0.1
        g, temp, pressure, density, c = env(1000000)
        assert abs(100 - round(temp, 2) / 1000.00 * 100) <= 0.1

    def test_density(self):
        env = pre.get_env_variables
        # Threshold set to ± 0.1%
        g, temp, pressure, density, c = env(0)
        assert abs(100 - round(density, 4) / 1.2252 * 100) <= 0.1
        g, temp, pressure, density, c = env(5000)
        assert abs(100 - round(density, 5) / 7.3643e-1 * 100) <= 0.1
        g, temp, pressure, density, c = env(11000)
        assert abs(100 - round(density, 5) / 3.6480e-1 * 100) <= 0.1
        g, temp, pressure, density, c = env(20000)
        assert abs(100 - round(density, 6) / 8.8910e-2 * 100) <= 0.1
        g, temp, pressure, density, c = env(70000)
        assert abs(100 - round(density, 9) / 8.2829e-5 * 100) <= 0.1
        g, temp, pressure, density, c = env(87000)
        assert abs(100 - round(density, 9) / 5.824e-6 * 100) <= 0.1
        g, temp, pressure, density, c = env(95000)
        assert abs(100 - round(density, 9) / 1.393e-6 * 100) <= 0.1
        g, temp, pressure, density, c = env(105000)
        assert abs(100 - round(density, 10) / 2.325e-7 * 100) <= 0.1
        g, temp, pressure, density, c = env(115000)
        assert abs(100 - round(density, 11) / 4.289e-8 * 100) <= 0.1
        g, temp, pressure, density, c = env(140000)
        assert abs(100 - round(density, 12) / 3.831e-9 * 100) <= 0.1
        g, temp, pressure, density, c = env(170000)
        assert abs(100 - round(density, 13) / 7.815e-10 * 100) <= 0.1
        g, temp, pressure, density, c = env(250000)
        assert abs(100 - round(density, 14) / 6.073e-11 * 100) <= 0.1
        g, temp, pressure, density, c = env(400000)
        assert abs(100 - round(density, 15) / 2.803e-12 * 100) <= 0.1
        g, temp, pressure, density, c = env(625000)
        assert abs(100 - round(density, 17) / 7.998e-14 * 100) <= 0.1
        g, temp, pressure, density, c = env(800000)
        assert abs(100 - round(density, 17) / 1.136e-14 * 100) <= 0.1
        g, temp, pressure, density, c = env(1000000)
        assert abs(100 - round(density, 18) / 3.561e-15 * 100) <= 0.1

    def test_speed_of_sound(self):
        env = pre.get_env_variables
        # Threshold set to ± 0.1%
        g, temp, pressure, density, c = env(1000)
        assert abs(100 - round(c, 1) / 336.4 * 100) <= 0.1
        g, temp, pressure, density, c = env(10000)
        assert abs(100 - round(c, 1) / 299.5 * 100) <= 0.1
        g, temp, pressure, density, c = env(30000)
        assert abs(100 - round(c, 1) / 301.7 * 100) <= 0.1
