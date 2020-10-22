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


class Parameters:

    def __init__(self,
                 engine=None,
                 fuel=None,
                 mass=None,
                 aero=None,
                 env=None,
                 sim=None
                 ):
        self._engine = engine
        self._fuel = fuel
        self._mass = mass
        self._aero = aero
        self._env = env
        self._sim = sim
        self.update_params()

    def __repr__(self):
        return 'simParametrs(' + str(self._params) + ')'

    @property
    def engine(self) -> list:
        return self._engine

    @engine.setter
    def engine(self, values: list):
        self._engine = values
        self.update_params()

    @property
    def fuel(self) -> list:
        return self._fuel

    @fuel.setter
    def fuel(self, values: list):
        self._fuel = values
        self.update_params()

    @property
    def mass(self) -> list:
        return self._mass

    @mass.setter
    def mass(self, values: list):
        self._mass = values
        self.update_params()

    @property
    def aero(self) -> list:
        return self._aero

    @aero.setter
    def aero(self, values: list):
        self._aero = values
        self.update_params()

    @property
    def env(self) -> list:
        return self._env

    @env.setter
    def env(self, values: list):
        self._env = values
        self.update_params()

    @property
    def sim(self) -> list:
        return self._sim

    @sim.setter
    def sim(self, values: list):
        self._sim = values
        self.update_params()

    @property
    def params(self):
        return self._params

    @params.setter
    def params(self, values):
        self._engine, self._fuel, self._mass, \
            self._aero, self._env, self._sim = values
        self.update_params()

    def update_params(self):
        self._params = {'engine': self._engine,
                        'fuel': self._fuel,
                        'mass': self._mass,
                        'aero': self._aero,
                        'env': self._env,
                        'sim': self._sim
                        }
