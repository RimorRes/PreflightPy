import math
class Environment:

    def __init__(self, calc_step = 1, g = 9.80665, M_air = 0.02896968, R = 8.314462618, gamma = 1.4, Pstatic = 101325):
        # Environmental Constants
        self.t = calc_step
        self.g = g
        self.M_air = M_air
        self.R = R
        self.gamma = gamma
        self.Pstatic = Pstatic

    def get_temp(self, h: float) -> float:
        if h <= 11000 :
            return 15.04 - 0.00649*h + 273.15
        elif 11000 < h <= 25000 :
            return -56.46 +273
        elif h > 25000 :
            return -131.21 + 0.00299*h + 273.15

    def get_pressure(self, h: float, T: float)-> float:
        try:
            return self.Pstatic * math.exp(-((self.M_air * self.g)/(self.R * T))* h)
        except OverflowError:
            return 0

    def get_density(self, P: float, T: float) -> float:
        N = 1
        m = self.M_air * N
        return (P * m )/(N * self.R * T)

    def get_c(self, T: float):
        return math.sqrt((self.gamma * self.R * T) / self.M_air)

    def get_status(self, h: float):
        self.T = self.get_temp(h)
        self.P = self.get_pressure(h, self.T)
        self.Rho = self.get_density(self.P, self.T)
        self.c = self.get_c(self.T)
