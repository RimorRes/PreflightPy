#!usr/bin/env python3

""" Preflight, a Python module for rocket flight simulation.
Copyright (C) 2019  RimorRes

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
from preflightpy._constants import g_zero, air_molar_mass, \
    gas_constant, air_gamma, earth_radius, \
    hb, pb, tb, lm


def atmo_heterosphere_equ(z: float, a, b, c, d, e):
    z_km = z/1000
    return math.exp(a * z_km**4
                    + b * z_km**3
                    + c * z_km**2
                    + d * z_km
                    + e
                    )


def get_geopotential_altitude(z: float) -> float:
    return earth_radius*z / (earth_radius+z)


def get_gravity(z: float) -> float:
    return g_zero * (earth_radius / (earth_radius + z))**2


def get_temp(z: float, h: float) -> tuple:
    if 0 <= h <= 11000:
        return 288.15 + (lm[0] * (h - 0)), 0
    elif 11000 < h <= 20000:
        return 216.65 + (lm[1] * (h - 11000)), 1
    elif 20000 < h <= 32000:
        return 216.65 + (lm[2] * (h - 20000)), 2
    elif 32000 < h <= 47000:
        return 228.65 + (lm[3] * (h - 32000)), 3
    elif 47000 < h <= 51000:
        return 270.65 + (lm[4] * (h - 47000)), 4
    elif 51000 < h <= 71000:
        return 270.65 + (lm[5] * (h - 51000)), 5
    elif 71000 < h <= 84852:
        return 214.65 + (lm[6] * (h - 71000)), 6
    elif 86000 < z <= 91000:
        return 186.87, 7
    elif 91000 < z <= 110000:
        if 91000 < z <= 100000:
            layer = 8
        else:
            layer = 9
        return (
            263.1905 - 76.3232 * math.sqrt(1 - ((z - 91000) / -19942.9)**2),  # noqa
            layer
            )
    elif 110000 < z <= 120000:
        return 240 + 0.012 * (z - 110000), 10
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
        else:
            layer = 16
        xi = (z - 120000) * (6356766 + 120000) / (6356766 + z)
        return 1000 - 640 * math.exp(-0.00001875 * xi), layer


def get_pressure(z: float, h: float, temp: float, b: int) -> float:

    if b <= 6:
        if lm[b] != 0:
            return pb[b] * (tb[b]/temp) ** \
                   (g_zero*air_molar_mass/(gas_constant*lm[b]))
        else:
            return pb[b] * math.exp(-g_zero * air_molar_mass * (h-hb[b])
                                    / (gas_constant*tb[b]))
    elif b == 7:
        return atmo_heterosphere_equ(
            z,
            0.000000,
            2.159582e-6,
            -4.836957e-4,
            -0.1425192,
            13.47530
            )
    elif b == 8:
        return atmo_heterosphere_equ(
            z,
            0.000000,
            3.304895e-5,
            -0.009062730,
            0.6516698,
            -11.03037
            )
    elif b == 9:
        return atmo_heterosphere_equ(
            z,
            0.000000,
            6.693926e-5,
            -0.01945388,
            1.719080,
            -47.75030
            )
    elif b == 10:
        return atmo_heterosphere_equ(
            z,
            0.000000,
            -6.539316e-5,
            0.02485568,
            -3.223620,
            135.9355
            )
    elif b == 11:
        return atmo_heterosphere_equ(
            z,
            2.283506e-7,
            -1.343221e-4,
            0.02999016,
            -3.055446,
            113.5764
            )
    elif b == 12:
        return atmo_heterosphere_equ(
            z,
            1.209434e-8,
            -9.692458e-6,
            0.003002041,
            -0.4523015,
            19.19151
            )
    elif b == 13:
        return atmo_heterosphere_equ(
            z,
            8.113942e-10,
            -9.822568e-7,
            4.687616e-4,
            -0.1231710,
            3.067409
            )
    elif b == 14:
        return atmo_heterosphere_equ(
            z,
            9.814674e-11,
            -1.654439e-7,
            1.148115e-4,
            -0.05431334,
            -2.011365
            )
    elif b == 15:
        return atmo_heterosphere_equ(
            z,
            -7.835161e-11,
            1.964589e-7,
            -1.657213e-4,
            0.04305869,
            -14.77132
            )
    elif b == 16:
        return atmo_heterosphere_equ(
            z,
            2.813255e-11,
            -1.120689e-7,
            1.695568e-4,
            -0.1188941,
            14.56718
            )


def get_density(z: float, pressure: float, temp: float, b) -> float:
    if b <= 6:
        return (pressure * air_molar_mass)/(gas_constant * temp)
    elif b == 7:
        return atmo_heterosphere_equ(
            z,
            0.000000,
            -3.322622E-06,
            9.111460E-04,
            -0.2609971,
            5.944694
            )
    elif b == 8:
        return atmo_heterosphere_equ(
            z,
            0.000000,
            2.873405e-05,
            -0.008492037,
            0.6541179,
            -23.62010
            )
    elif b == 9:
        return atmo_heterosphere_equ(
            z,
            -1.240774e-05,
            0.005162063,
            -0.8048342,
            55.55996,
            -1443.338
            )
    elif b == 10:
        return atmo_heterosphere_equ(
            z,
            0.00000,
            -8.854164e-05,
            0.03373254,
            -4.390837,
            176.5294
            )
    elif b == 11:
        return atmo_heterosphere_equ(
            z,
            3.661771e-07,
            -2.154344e-04,
            0.04809214,
            -4.884744,
            172.3597
            )
    elif b == 12:
        return atmo_heterosphere_equ(
            z,
            1.906032e-08,
            -1.527799E-05,
            0.004724294,
            -0.6992340,
            20.50921
            )
    elif b == 13:
        return atmo_heterosphere_equ(
            z,
            1.199282e-09,
            -1.451051e-06,
            6.910474e-04,
            -0.1736220,
            -5.321644
            )
    elif b == 14:
        return atmo_heterosphere_equ(
            z,
            1.140564e-10,
            -2.130756e-07,
            1.570762e-04,
            -0.07029296,
            -12.89844
            )
    elif b == 15:
        return atmo_heterosphere_equ(
            z,
            8.105631e-12,
            -2.358417e-09,
            -2.635110e-06,
            -0.01562608,
            -20.02246
            )
    elif b == 16:
        return atmo_heterosphere_equ(
            z,
            -3.701195e-12,
            -8.608611e-09,
            5.118829e-05,
            -0.06600998,
            -6.137674
            )


def get_sonic(temp: float) -> float:
    return math.sqrt((air_gamma * gas_constant * temp) / air_molar_mass)


def get_env_variables(z: float):
    h = round(get_geopotential_altitude(z), 0)
    g = get_gravity(z)
    temp, b = get_temp(z, h)
    pressure = get_pressure(z, h, temp, b)
    density = get_density(z, pressure, temp, b)
    c = get_sonic(temp)
    return g, temp, pressure, density, c
