#!usr/bin/env python3

import math
class Environment:

    def __init__(self, vars):
        # Environmental Constants
        self.elev, self.t, self.g, self.M_air, self.R, self.gamma, self.Pstatic = vars

    def get_temp(self, h: float) -> float:
        if 0 <= h < 11000:
            return 288.15 + (-0.0065*(h-0))
        elif 11000 <= h < 20000:
            return 216.65 + (0.0*(h-11000))
        elif 20000 <= h < 32000:
            return 216.65 + (0.001*(h-20000))
        elif 32000 <= h < 47000:
            return 228.65 + (0.0028*(h-32000))
        elif 47000 <= h < 51000:
            return 270.65 + (0.0*(h-47000))
        elif 51000 <= h < 71000:
            return 270.65 + (-0.0028*(h-51000))
        elif 71000 <= h:
            return 214.65 + (-0.002*(h-71000)) if not 214.65 + (-0.002*(h-71000)) < 0 else 0

    def get_pressure(self, h: float, T: float)-> float:
        try:
            return self.Pstatic * math.exp(-((self.M_air * self.g)/(self.R * T))* h)
        except OverflowError:
            return 0

    def get_density(self, P: float, T: float) -> float:
        V = 1
        n = (P*V)/(self.R*T)
        m = self.M_air * n
        return (P * m )/(n * self.R * T)

    def get_c(self, T: float):
        return math.sqrt((self.gamma * self.R * T) / self.M_air)

    def get_status(self, h: float):
        self.T = self.get_temp(h)
        self.P = self.get_pressure(h, self.T)
        self.Rho = self.get_density(self.P, self.T)
        self.c = self.get_c(self.T)
