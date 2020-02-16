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
import csv
import matplotlib.pyplot as plt


class System:
    def __init__(self, params, env, burn_time: float):
        p = params
        # Environment
        self.env = env
        # Burn time
        self.num_steps = int(burn_time/self.env.t)
        self.burn_time = self.num_steps * self.env.t
        # Engine specs
        self.isp, self.Fthrust = p.package[0]
        # Fuel Specs
        self.OFratio, self.Reserve = p.package[1]
        # Flow Rate
        self.w = (self.Fthrust/9.81)/self.isp
        self.dF = self.w * (1/(self.OFratio+1))
        self.dOx = (self.w - self.dF)
        # Fuel & Oxidizer
        self.F = (self.dF * self.burn_time)/(1 - self.Reserve/100)
        self.Ox = (self.dOx * self.burn_time)/(1 - self.Reserve/100)
        # Mass
        self.frameM = p.package[2][0]
        # Aerodynamics
        self.Cd, self.Aproj = p.package[3]
        # Output
        self.logout, self.csvout = p.package[4]

        open(self.logout, "w").close()

        self.field_names = [
            "t",
            "Fthrust",
            "Fdrag",
            "m",
            "v",
            "Mach",
            "a",
            "altitude",
            "asl",
            "twr",
            "maxV",
            "maxMach",
            "maxAcc",
            "minAcc",
            "maxG",
            "minG"
        ]
        with open(self.csvout, "w", newline="") as f:
            csv_writer = csv.writer(f)
            csv_writer.writerow(self.field_names)
            f.close()

# Flight
    def launch(self):
        """Runs a simulation within the given parameters."""
        # Variable setup
        self.altitude = 0
        self.asl = self.altitude + self.env.elev
        self.calc_mass()
        self.env.get_status(self.asl)
        self.calc_twr()
        self.Fdrag = 0
        self.v = 0
        self.maxV = 0
        self.Mach = 0
        self.maxMach = 0
        self.maxAcc = 0
        self.maxG = 0
        self.minAcc = 0
        self.minG = 0
        self.a = 0
        self.j = 0
        self.s = 0
        self.t = 0

        # Used by matplotlib
        self.plot_data = [
            [],  # index:0 time
            [],  # index:1 altitude
            [],  # index:2 velocity
            [],  # index:3 speed of sound
            [],  # index:4 acceleration
            [],  # index:5 jerk
            [],  # index:6 snap
            [],  # index:7 drag
            [],  # index:8 temperature
            [],  # index:9 pressure
            []   # index:10 density
            ]

        # Accelaration phase
        for i in range(self.num_steps):
            # Output management
            self.add_data()
            # Environment-related
            self.update_env()
            # Accelaration/derivative-related
            self.calc_acc()
            self.calc_additional_derivatives()
            # Position-related
            self.set_altitude()
            # Velocity-related
            self.calc_velocity()
            # Force-related
            self.calc_drag()
            self.calc_twr()
            # Mass-related
            self.remove_fuel()
            self.calc_mass()
            # Time-related
            self.t += self.env.t

            if self.twr < 1:
                raise RuntimeError("TWR below 1 : {}".format(self.twr))

            if self.a > self.maxAcc:
                self.maxAcc = self.a
                self.maxG = self.maxAcc/self.env.g

            if self.v > self.maxV:
                self.maxV = self.v
                self.maxMach = self.Mach

        self.Fthrust = 0

        # Deceleration phase
        while self.v > 0:
            # Output management
            self.add_data()
            # Environment-related
            self.update_env()
            # Accelaration/derivative-related
            self.calc_acc()
            self.calc_additional_derivatives()
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
            self.t += self.env.t

            if self.a < self.minAcc:
                self.minAcc = self.a
                self.minG = self.minAcc/self.env.g

        self.output(
            "maxV",
            "maxMach",
            "maxAcc",
            "minAcc",
            "maxG",
            "minG"
        )

    def suicide_burn(self):
        """Run a suicide burn simulation, will affct ascent simulation."""
        self.Vt = math.sqrt((2 * self.m * self.env.g) / (self.env.Rho * self.Aproj * self.Cd))  # noqa

# Mass
    def calc_mass(self):
        self.fuelM = (self.Ox + self.F)
        self.m = self.fuelM + self.frameM

    def remove_fuel(self):
        self.Ox -= self.dOx * self.env.t
        self.F -= self.dF * self.env.t

# Position
    def set_altitude(self):
        self.altitude += self.v * self.env.t + (self.a * self.env.t**2)/2  # noqa
        self.asl = self.altitude + self.env.elev

# Derivatives of position
    def calc_velocity(self):
        self.v += self.a * self.env.t
        self.Mach = self.v/self.env.c

    def calc_acc(self):
        self.a = (self.Fthrust - (self.m * 9.81 + self.Fdrag)) / self.m

    def calc_additional_derivatives(self):
        self.j = (self.a - self.plot_data[4][-1]) / self.env.t
        self.s = (self.j - self.plot_data[5][-1]) / self.env.t

# Forces
    def calc_drag(self):
        self.Fdrag = 0.5 * (self.env.Rho * self.v**2 * self.Cd * self.Aproj)

    def calc_twr(self):
        self.twr = self.Fthrust / (self.m * 9.81)

# Environment
    def update_env(self):
        self.env.get_status(self.asl)

# Ouput
    def output(self, *args):
        with open(self.logout, 'a') as f:
            for arg in args:
                value = str(round(eval(arg, self.__dict__), 5)).ljust(10)
                f.write('\t' + arg + ' : ' + value + '\t')
            f.write('\n')
            f.close()

        values = []
        for field in self.field_names:
            value = str(round(eval(field, self.__dict__), 5))
            values.append(value)

        with open(self.csvout, "a", newline="") as f:
            csv_writer = csv.writer(f)
            csv_writer.writerow(values)
            f.close()

    def add_data(self):
        self.plot_data[0].append(self.t)
        self.plot_data[1].append(self.altitude)
        self.plot_data[2].append(self.v)
        self.plot_data[3].append(self.env.c)
        self.plot_data[4].append(self.a)
        self.plot_data[5].append(self.j)
        self.plot_data[6].append(self.s)
        self.plot_data[7].append(self.Fdrag)
        self.output(
            "t",
            "Fthrust",
            "Fdrag",
            "m",
            "v",
            "Mach",
            "a",
            "altitude",
            "asl",
            "twr"
            )


def plot(burn_time: float, plot_data: list):
    pd = plot_data
    t = burn_time
    plt.figure(1)
    plt.plot(pd[0], pd[1])
    plt.xlabel("time (s)")
    plt.ylabel("Altitude (m)")
    plt.title("{} s burn time".format(t))
    plt.grid(True)

    plt.figure(2)
    plt.plot(pd[0], pd[2], pd[0], pd[3])
    plt.xlabel("time (s)")
    plt.ylabel("Velocity (m/s) (orange: sound, blue: rocket)")
    plt.title("{} s burn time".format(t))
    plt.grid(True)

    plt.figure(3)
    plt.plot(pd[0], pd[4])
    plt.xlabel("time (s)")
    plt.ylabel("Acceleration (m/s2)")
    plt.title("{} s burn time".format(t))
    plt.grid(True)

    plt.figure(4)
    plt.subplot(2, 1, 1)
    plt.plot(pd[0], pd[5])
    plt.ylabel("Jerk (m/s3)")
    plt.title("{} s burn time".format(t))
    plt.grid(True)
    plt.subplot(2, 1, 2)
    plt.plot(pd[0], pd[6], 'r-')
    plt.xlabel("time (s)")
    plt.ylabel("Snap (m/s4)")
    plt.grid(True)

    plt.figure(5)
    plt.plot(pd[0], pd[7])
    plt.xlabel("time (s)")
    plt.ylabel("Drag (N)")
    plt.title("{} s burn time".format(t))
    plt.grid(True)

    plt.show()
