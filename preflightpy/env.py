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
        self.elev, self.t, self.g, self.M_air, self.R, self.gamma, self.Pstatic = vars
        self.hb = [0, 11000, 20000, 32000, 47000, 51000, 71000]
        self.Pb = [101325, 22632.1, 5474.89, 868.019, 110.906, 66.9389, 3.95642]
        self.Tb = [288.15, 216.65, 216.65, 228.65, 270.65, 270.65, 214.65]
        self.Lm = [-0.0065, 0.0, 0.001, 0.0028, 0.0, -0.0028, -0.002]

    def get_geopotential_altitude(self, r: float, z: float) -> float:
        return r*z / (r+z)

    def get_temp(self, h: float) -> float:
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
        elif 71000 < h:
            return (214.65 + (self.Lm[6]*(h-71000)), 6)

    def get_pressure(self, z: float, h: float, T: float, b: int)-> float:

        def equ(a, b, c, d, e):
            return math.exp( a * z**4 + b * z**3 + c * z**2 + d * z + e)

        if b <= 6:
            if self.Lm[b] != 0:
                return self.Pb[b] * ( self.Tb[b]/T )**(self.g*self.M_air/(self.R*self.Lm[b]))
            else:
                return self.Pb[b] * math.exp( -self.g * self.M_air * (h-self.hb[b]) / (self.R*self.Tb[b]) )
        elif b == 7:
            return equ(0.000000, 2.159582*10**(-6),	-4.836957*10**(-4),	-0.1425192,	13.47530)
        elif b == 8:
            return equ(0.000000, 3.304895*10**(-5),	-0.009062730, 0.6516698, -11.03037)
        elif b == 9:
            return equ(0.000000, 6.693926*10**(-5),	-0.01945388, 1.719080, -47.75030)
        elif b == 10:
            return equ(0.000000, -6.539316*10**(-5), 0.02485568, -3.223620, 135.9355)
        elif b == 11:
            return equ(2.283506*10**(-7), -1.343221*10**(-4), 0.02999016, -3.055446, 113.5764)
        elif b == 12:
            return equ(1.209434*10**(-8), -9.692458*10**(-6), 0.003002041, -0.4523015, 19.19151)
        elif b == 13:
            return equ(8.113942*10**(-10), -9.822568*10**(-7), 4.687616*10**(-4), -0.1231710, 3.067409)
        elif b == 14:
            return equ(9.814674*10**(-11), -1.654439*10**(-7), 1.148115*10**(-4), -0.05431334, -2.011365)
        elif b == 15:
            return equ(-7.835161*10**(-11), 1.964589*10**(-7), -1.657213*10**(-4), 0.04305869, -14.77132)
        elif b == 16:
            return equ(2.813255*10**(-11), -1.120689*10**(-7), 1.695568*10**(-4), -0.1188941, 14.56718)

    def get_density(self, P: float, T: float) -> float:
        V = 1
        n = (P*V)/(self.R*T)
        m = self.M_air * n
        return (P * m )/(n * self.R * T)

    def get_c(self, T: float):
        return math.sqrt((self.gamma * self.R * T) / self.M_air)

    def get_status(self, z: float):
        h = round(self.get_geopotential_altitude(6378137, z),0)
        self.T, b = self.get_temp(h)
        self.P = self.get_pressure(z, h, self.T, b)
        self.Rho = self.get_density(self.P, self.T)
        self.c = self.get_c(self.T)
