#!usr/bin/env python3

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

    def get_pressure(self, h: float, T: float, b: int)-> float:
        if self.Lm[b] != 0:
            return self.Pb[b] * ( self.Tb[b]/T )**(self.g*self.M_air/(self.R*self.Lm[b]))
        else:
            return self.Pb[b] * math.exp( -self.g * self.M_air * (h-self.hb[b]) / (self.R*self.Tb[b]) )


    def get_density(self, P: float, T: float) -> float:
        V = 1
        n = (P*V)/(self.R*T)
        m = self.M_air * n
        return (P * m )/(n * self.R * T)

    def get_c(self, T: float):
        return math.sqrt((self.gamma * self.R * T) / self.M_air)

    def get_status(self, z: float):
        h = round(self.get_geopotential_altitude(6378137, z),0)
        print(h)
        self.T, b = self.get_temp(h)
        print(self.T, b)
        self.P = self.get_pressure(h, self.T, b)
        print(self.P)
        self.Rho = self.get_density(self.P, self.T)
        self.c = self.get_c(self.T)
