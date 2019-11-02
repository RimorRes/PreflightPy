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
        elif 71000 < h <= 84856:
            return (214.65 + (self.Lm[6]*(h-71000)), 6)
        elif 86000 < z <= 91000:
            return (186.67, 7)
        elif 91000 < z <= 110000:
            return (263.1905 - 76.3232 * math.sqrt(1 - ((z - 91000) / -19942.9)**2), 8)
        elif 110000 < z <= 120000:
            return (240 + 0.012 * (z - 110000), 9)
        elif 120000 < z <= 1000000:
            xi = (z - 120000) * (6356766 + 120000) / (6356766 + z)
            return (1000 - 640 * math.exp(-0.00001875 * xi), 10)

    def get_pressure(self, h: float, T: float, b: int)-> float:
        if b <= 6:
            if self.Lm[b] != 0:
                return self.Pb[b] * ( self.Tb[b]/T )**(self.g*self.M_air/(self.R*self.Lm[b]))
            else:
                return self.Pb[b] * math.exp( -self.g * self.M_air * (h-self.hb[b]) / (self.R*self.Tb[b]) )


    def get_density(self, P: float, T: float, b) -> float:
        if b <= 6:
            V = 1
            n = (P*V)/(self.R*T)
            m = self.M_air * n
            return (P * m )/(n * self.R * T)

    def get_c(self, T: float):
        return math.sqrt((self.gamma * self.R * T) / self.M_air)

    def get_status(self, z: float):
        h = round(self.get_geopotential_altitude(6356766, z), 0)
        self.T, b = self.get_temp(z, h)
        self.P = self.get_pressure(h, self.T, b)
        self.Rho = self.get_density(self.P, self.T, b)
        self.c = self.get_c(self.T)
