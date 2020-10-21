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

import json


class Parameters:

    def __init__(self, path="preflight/case.params"):

        self.package = []
        file = open(path, 'r')
        j = json.load(file)

        for subgroup in j.values():
            self.package.append([self.cast(x) for x in subgroup.values()])

        file.close()

    def cast(self, x):
        try:
            return float(x)
        except Exception:
            return str(x)
