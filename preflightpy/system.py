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
import numpy as np
from preflightpy.env import get_env_variables
from preflightpy._constants import g_0


class System:
    def __init__(self, params):
        p = params

        # Engine specs
        self.isp, self.avg_thrust, self.burn_time, \
            self.thrust_curve_x, self.thrust_curve_y = p.params['engine']

        # Fuel Specs
        fuel_reserve = p.params['fuel'][0]

        # Flow Rate
        self.avg_mass_flow_rate = (self.avg_thrust / g_0) / self.isp

        # Fuel & Oxidizer
        self.propellant_mass = (self.avg_mass_flow_rate * self.burn_time) \
            / (1 - fuel_reserve / 100)

        # Mass
        self.dry_mass = p.params['mass'][0]

        # Aerodynamics
        self.Cd, self.cross_section = p.params['aero']

        # Environment
        self.elevation = p.params['env'][0]

        # Simulation settings
        self.dt = p.params['sim'][0]

        self.num_steps = math.floor(self.burn_time / self.dt)

        # Initialisation
        self.t = 0
        self.altitude = 0
        self.asl = self.altitude + self.elevation
        self.calc_mass()
        self.update_env()
        self.calc_thrust()
        self.calc_twr()
        self.drag = 0
        self.v = 0
        self.mach = 0
        self.a = 0

    # Flight
    def launch(self):
        """
        Runs a simulation within the given parameters.
        """

        # Accelaration phase
        for i in range(self.num_steps):
            yield self.altitude
            # Environment-related
            self.update_env()
            # Thrust-related
            self.calc_thrust()
            # Accelaration
            self.calc_acc()
            # Position-related
            self.set_altitude()
            # Velocity-related
            self.calc_velocity()
            # Force-related
            self.calc_drag()
            self.calc_twr()
            # Mass-related
            self.calc_propellant()
            self.calc_mass()
            # Time-related
            self.t += self.dt

        self.thrust = 0

        # Deceleration phase
        while self.v >= 0:
            yield self.altitude
            # Environment-related
            self.update_env()
            # Acceleration
            self.calc_acc()
            # Position-related
            self.set_altitude()
            # Velocity-related
            self.calc_velocity()
            # Force-related
            self.calc_drag()
            self.calc_twr()
            # Mass-related
            self.calc_mass()
            # Time-related
            self.t += self.dt

    # Mass
    def calc_mass(self):
        self.mass = self.propellant_mass + self.dry_mass

    def calc_propellant(self):
        self.mass_flow_rate = (self.thrust / g_0) / self.isp
        self.propellant_mass -= self.mass_flow_rate * self.dt

    # Position
    def set_altitude(self):
        self.altitude += self.v * self.dt \
            + (self.a * self.dt**2)/2
        self.asl = self.altitude + self.elevation

    # Derivatives of position
    def calc_velocity(self):
        self.v += self.a * self.dt
        self.mach = self.v/self.c

    def calc_acc(self):
        self.a = (self.thrust - (self.mass * self.g + self.drag)) / self.mass

    # Forces
    def calc_thrust(self):
        self.thrust = np.interp(self.t,
                                self.thrust_curve_x,
                                self.thrust_curve_y
                                )

    def calc_drag(self):
        self.drag = 0.5 \
            * (self.air_rho * self.v**2 * self.Cd * self.cross_section)

    def calc_twr(self):
        self.twr = self.thrust / (self.mass * self.g)

    # Environment
    def update_env(self):
        self.g, self.temp, self.pressure, self.air_rho, self.c \
            = get_env_variables(self.asl)
