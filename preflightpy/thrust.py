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

class Thrust_Curve:

    def get_curve(self, path):

        with(open(path)) as f:

            csv_reader = csv.reader(f)
            curve_points = {}

            for row in csv_reader:
                curve_points.update({
                    float(row[0]): float(row[1])
                })

            f.close()

        return curve_points

    def calc_points(self, curve_points: dict, step: float):
        new = {}
        for index in range(len(curve_points)-1):
            pass
