#!usr/bin/env python3

""" Preflight, a Python module for rocket flight simulation.
Copyright (C) 2019  Oxyde2

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <https://www.gnu.org/licenses/>.

You can contact the author at the following email address:
iorbital.projects@gmail.com """

import math


class Environment:

    def __init__(self, vars):
        # Environmental Constants
        self.elev, self.t, self.g, self.M_air, self.R, self.gamma, self.Pstatic = vars  # noqa
        self.g_zero = self.g
        self.Re = 6356766
        self.hb = [  # Layer base altitudes
            0,
            11000,
            20000,
            32000,
            47000,
            51000,
            71000
            ]
        self.Pb = [  # Layer base pressures
            101325,
            22632.1,
            5474.89,
            868.019,
            110.906,
            66.9389,
            3.95642
            ]
        self.Tb = [  # Layer base temperatures
            288.15,
            216.65,
            216.65,
            228.65,
            270.65,
            270.65,
            214.65
            ]
        self.Lm = [  # Layer lapse rates
            -0.0065,
            0.0,
            0.001,
            0.0028,
            0.0,
            -0.0028,
            -0.002
            ]

    def get_geopotential_altitude(self, z: float) -> float:
        return self.Re*z / (self.Re+z)

    def atmo_heterosphere_equ(self, z: float, a, b, c, d, e):
        z_km = z/1000
        return math.exp(a * z_km**4 + b * z_km**3 + c * z_km**2 + d * z_km + e)  # noqa

    def get_gravity(self, z: float) -> float:
        return self.g_zero * (self.Re / (self.Re + z))**2

    def get_temp(self, z: float, h: float) -> float:
        if 0 <= h <= 11000:
            return (288.15 + (self.Lm[0]*(h-0)), 0)
        elif 11000 < h <= 20000:
            return (216.65 + (self.Lm[1]*(h-11000)), 1)
        elif 20000 < h <= 32000:
            return (216.65 + (self.Lm[2]*(h-20000)), 2)
        elif 32000 < h <= 47000:
            return (228.65 + (self.Lm[3]*(h-32000)), 3)
        elif 47000 < h <= 51000:
            return (270.65 + (self.Lm[4]*(h-47000)), 4)
        elif 51000 < h <= 71000:
            return (270.65 + (self.Lm[5]*(h-51000)), 5)
        elif 71000 < h <= 84852:
            return (214.65 + (self.Lm[6]*(h-71000)), 6)
        elif 86000 < z <= 91000:
            return (186.87, 7)
        elif 91000 < z <= 110000:
            if 91000 < z <= 100000:
                layer = 8
            elif 100000 < z <= 110000:
                layer = 9
            return (
                263.1905 - 76.3232 * math.sqrt(1 - ((z - 91000) / -19942.9)**2),  # noqa
                layer
                )
        elif 110000 < z <= 120000:
            return (240 + 0.012 * (z - 110000), 10)
        elif 120000 < z <= 1000000:
            if 120000 < z <= 150000:
                layer = 11
            elif 150000 < z <= 200000:
                layer = 12
            elif 200000 < z <= 300000:
                layer = 13
            elif 300000 < z <= 500000:
                layer = 14
            elif 500000 < z <= 750000:
                layer = 15
            elif 750000 < z <= 1000000:
                layer = 16
            xi = (z - 120000) * (6356766 + 120000) / (6356766 + z)
            return (1000 - 640 * math.exp(-0.00001875 * xi), layer)

    def get_pressure(self, z: float, h: float, T: float, b: int) -> float:

        if b <= 6:
            if self.Lm[b] != 0:
                return self.Pb[b] * (self.Tb[b]/T)**(self.g*self.M_air/(self.R*self.Lm[b]))  # noqa
            else:
                return self.Pb[b] * math.exp(-self.g * self.M_air * (h-self.hb[b]) / (self.R*self.Tb[b]))  # noqa
        elif b == 7:
            return self.atmo_heterosphere_equ(
                z,
                0.000000,
                2.159582e-6,
                -4.836957e-4,
                -0.1425192,
                13.47530
                )
        elif b == 8:
            return self.atmo_heterosphere_equ(
                z,
                0.000000,
                3.304895e-5,
                -0.009062730,
                0.6516698,
                -11.03037
                )
        elif b == 9:
            return self.atmo_heterosphere_equ(
                z,
                0.000000,
                6.693926e-5,
                -0.01945388,
                1.719080,
                -47.75030
                )
        elif b == 10:
            return self.atmo_heterosphere_equ(
                z,
                0.000000,
                -6.539316e-5,
                0.02485568,
                -3.223620,
                135.9355
                )
        elif b == 11:
            return self.atmo_heterosphere_equ(
                z,
                2.283506e-7,
                -1.343221e-4,
                0.02999016,
                -3.055446,
                113.5764
                )
        elif b == 12:
            return self.atmo_heterosphere_equ(
                z,
                1.209434e-8,
                -9.692458e-6,
                0.003002041,
                -0.4523015,
                19.19151
                )
        elif b == 13:
            return self.atmo_heterosphere_equ(
                z,
                8.113942e-10,
                -9.822568e-7,
                4.687616e-4,
                -0.1231710,
                3.067409
                )
        elif b == 14:
            return self.atmo_heterosphere_equ(
                z,
                9.814674e-11,
                -1.654439e-7,
                1.148115e-4,
                -0.05431334,
                -2.011365
                )
        elif b == 15:
            return self.atmo_heterosphere_equ(
                z,
                -7.835161e-11,
                1.964589e-7,
                -1.657213e-4,
                0.04305869,
                -14.77132
                )
        elif b == 16:
            return self.atmo_heterosphere_equ(
                z,
                2.813255e-11,
                -1.120689e-7,
                1.695568e-4,
                -0.1188941,
                14.56718
                )

    def get_density(self, z: float, P: float, T: float, b) -> float:
        if b <= 6:
            return (P * self.M_air)/(self.R * T)
        elif b == 7:
            return self.atmo_heterosphere_equ(
                z,
                0.000000,
                -3.322622E-06,
                9.111460E-04,
                -0.2609971,
                5.944694
                )
        elif b == 8:
            return self.atmo_heterosphere_equ(
                z,
                0.000000,
                2.873405e-05,
                -0.008492037,
                0.6541179,
                -23.62010
                )
        elif b == 9:
            return self.atmo_heterosphere_equ(
                z,
                -1.240774e-05,
                0.005162063,
                -0.8048342,
                55.55996,
                -1443.338
                )
        elif b == 10:
            return self.atmo_heterosphere_equ(
                z,
                0.00000,
                -8.854164e-05,
                0.03373254,
                -4.390837,
                176.5294
                )
        elif b == 11:
            return self.atmo_heterosphere_equ(
                z,
                3.661771e-07,
                -2.154344e-04,
                0.04809214,
                -4.884744,
                172.3597
                )
        elif b == 12:
            return self.atmo_heterosphere_equ(
                z,
                1.906032e-08,
                -1.527799E-05,
                0.004724294,
                -0.6992340,
                20.50921
                )
        elif b == 13:
            return self.atmo_heterosphere_equ(
                z,
                1.199282e-09,
                -1.451051e-06,
                6.910474e-04,
                -0.1736220,
                -5.321644
                )
        elif b == 14:
            return self.atmo_heterosphere_equ(
                z,
                1.140564e-10,
                -2.130756e-07,
                1.570762e-04,
                -0.07029296,
                -12.89844
                )
        elif b == 15:
            return self.atmo_heterosphere_equ(
                z,
                8.105631e-12,
                -2.358417e-09,
                -2.635110e-06,
                -0.01562608,
                -20.02246
                )
        elif b == 16:
            return self.atmo_heterosphere_equ(
                z,
                -3.701195e-12,
                -8.608611e-09,
                5.118829e-05,
                -0.06600998,
                -6.137674
                )

    def get_c(self, T: float) -> float:
        return math.sqrt((self.gamma * self.R * T) / self.M_air)

    def get_status(self, z: float):
        h = round(self.get_geopotential_altitude(z), 0)
        self.g = self.get_gravity(z)
        self.T, b = self.get_temp(z, h)
        self.P = self.get_pressure(z, h, self.T, b)
        self.Rho = self.get_density(z, self.P, self.T, b)
        self.c = self.get_c(self.T)
