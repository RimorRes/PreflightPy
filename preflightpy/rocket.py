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


import numpy as np
from preflightpy._constants import g_0, air_rho_0
from scipy.spatial.transform import Rotation


class Fuel:  # TODO: Accommodate for liquid and hybrid engines
    pass


class Engine:

    def __init__(self,
                 isp,
                 avg_thrust,
                 burn_time,
                 thrust_curve,
                 mass,
                 rel_pos,
                 moi,
                 rel_rot=np.array([0, 0]),
                 gimbal_limits=np.array([[0, 0], [0, 0]])
                 ):
        # Motor Specs
        self.isp = isp
        self.avg_thrust = avg_thrust
        self.burn_time = burn_time
        self.thrust_curve = thrust_curve
        # Linear Motion
        self.mass = mass
        self.rel_pos = rel_pos
        # Rotational Motion
        self.moi = moi
        # Parallel axis theorem
        self.abs_moi = np.array([self.moi[0] +
                                 (self.rel_pos[1] ** 2 + self.rel_pos[2] ** 2)
                                 * self.mass,
                                 self.moi[1] +
                                 (self.rel_pos[0] ** 2 + self.rel_pos[2] ** 2)
                                 * self.mass,
                                 self.moi[2] +
                                 (self.rel_pos[0] ** 2 + self.rel_pos[1] ** 2)
                                 * self.mass
                                 ])
        self.rel_rot = rel_rot  # Spherical coordinates; Rocket (& thrust) up
        self.gimbal = np.array([0, 0])  # Spherical coordinates
        self.gimbal_limits = gimbal_limits  # Spherical coordinates
        # Forces and torques
        self.thrust_scalar = self.calc_thrust_scalar(0)
        self.rel_thrust_vec = self.calc_rel_thrust_vector()

    def calc_thrust_scalar(self, t):
        x, y = self.thrust_curve
        thrust = np.interp(t, x, y)

        return thrust

    def calc_rel_thrust_vector(self):
        theta, phi = self.gimbal + self.rel_rot
        vec = np.array([self.thrust_scalar * np.sin(theta) * np.cos(phi),
                        self.thrust_scalar * np.sin(theta) * np.sin(phi),
                        self.thrust_scalar * np.cos(theta)
                        ])

        return vec


class Rocket:

    def __init__(self,
                 engines,
                 com,
                 moi,
                 dry_mass,
                 cs_area,
                 cd,
                 pos=np.array([0, 0, 0]),
                 rot=np.array([np.pi/2, 0, 0])
                 ):
        self.engines = engines
        self.dry_com = com
        self.com = self.calc_center_of_mass()
        # Linear Motion
        self.dry_mass = dry_mass
        self.mass = self.calc_mass()
        self.pos = pos
        self.vel = np.array([0, 0, 0])
        self.acc = np.array([0, 0, 0])
        # Rotational Motion
        self.dry_moi = moi
        self.moi = self.calc_moment_of_inertia()
        self.rot = rot
        self.ang_vel = np.array([0, 0, 0])
        self.ang_acc = np.array([0, 0, 0])
        # Aerodynamics
        self.cs_area = cs_area
        self.cd = cd
        # Forces
        self.weight = self.calc_weight(g_0)
        self.total_thrust = self.calc_total_thrust()
        self.drag = self.calc_drag(air_rho_0)
        self.total_external_force = self.calc_total_external_force()
        # Torques
        self.total_torque = self.calc_total_torque()

    def calc_center_of_mass(self):
        """
        Rocket pointing up
        Relative positions should be measured relative to the tip of the rocket
        CoM is measured from the tip of the rocket
        """
        engine_masses = np.array([0, 0, 0])
        engine_weighted_position = np.array([0, 0, 0])
        for e in self.engines:
            engine_masses += e.mass
            engine_weighted_position += e.mass * e.rel_pos
        com = (self.dry_com * self.dry_mass + engine_weighted_position) \
            / (self.dry_mass + engine_masses)

        return com

    def calc_mass(self):
        total_mass = self.dry_mass
        for e in self.engines:
            total_mass += e.mass

        return total_mass

    def calc_position(self, dt):
        new_pos = self. pos + self.vel * dt + (self.acc * dt ** 2) / 2

        return new_pos

    def calc_velocity(self, dt):
        new_vel = self.vel + self.acc * dt

        return new_vel

    def calc_acceleration(self):
        new_acc = self.total_external_force / self.mass

        return new_acc

    def calc_moment_of_inertia(self):
        """
        Rocket pointing up
        X axis: pitch
        Y axis: yaw
        Z axis: roll
        MoI about X, Y, and Z axes with origin being CoM
        """
        moi = self.dry_moi
        for e in self.engines:
            moi += e.abs_moi

        return moi

    def calc_angular_position(self, dt):
        new_rot = self.rot + self.ang_vel * dt + (self.ang_acc * dt ** 2) / 2

        return new_rot

    def calc_angular_velocity(self, dt):
        new_ang_vel = self.ang_vel + self.ang_acc * dt

        return new_ang_vel

    def calc_angular_acceleration(self):
        new_ang_acc = self.total_torque / self.moi

        return new_ang_acc

    def calc_weight(self, g):
        """
        Returns weight vector.
        """
        weight = self.mass * np.array([0, 0, -g])

        return weight

    def calc_total_thrust(self):
        """
        Returns thrust vector.
        """
        total_rel_vec = np.array([0, 0, 0])
        for e in self.engines:
            total_rel_vec += e.rel_thrust_vec

        gamma, beta, alpha = self.rot
        matrix = [[np.cos(alpha)*np.cos(beta),
                   np.cos(alpha)*np.sin(beta) *
                   np.sin(gamma)-np.sin(alpha)*np.cos(gamma),
                   np.cos(alpha)*np.sin(beta) *
                   np.cos(gamma)+np.sin(alpha)*np.sin(gamma)
                   ],
                  [np.sin(alpha)*np.cos(beta),
                   np.sin(alpha)*np.sin(beta) *
                   np.sin(gamma)+np.cos(alpha)*np.cos(gamma),
                   np.sin(alpha)*np.sin(beta) *
                   np.cos(gamma)-np.cos(alpha)*np.sin(gamma)
                   ],
                  [-np.sin(beta),
                   np.cos(beta)*np.sin(gamma),
                   np.cos(beta)*np.cos(gamma)
                   ]
                  ]
        rotation = Rotation.from_matrix(matrix)
        total_thrust = rotation.apply(total_rel_vec)

        return total_thrust

    def calc_drag(self, air_rho):
        """
        Returns drag vector.
        """
        drag = 0.5 * (air_rho * self.vel ** 2 * self.cd * self.cs_area)

        return drag

    def calc_total_external_force(self):
        """
        Returns force vector equal to the sum of all external
        force vectors.
        """
        total_ext = self.weight + self.total_thrust + self.drag

        return total_ext

    def calc_total_torque(self):
        total_torque = np.array([0, 0, 0])
        for e in self.engines:
            position_vec = self.com - e.rel_pos
            total_torque += np.cross(position_vec, e.rel_thrust_vec)

        return total_torque
