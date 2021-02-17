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


class Part:

    def __init__(self,
                 name,
                 mass,
                 com,
                 rel_pos,
                 moi,
                 rel_rot
                 ):
        # Mass
        self.mass = mass
        self.com = com
        # Position
        self.rel_pos = rel_pos
        # Rotation
        self.moi = moi
        self.abs_moi = self.calc_abs_moi()
        self.rel_rot = rel_rot  # TODO: ZYX Euler angles? Also its useles rn so modify it so it affects MoI
        # Miscellaneous
        self.name = name

    def update_part(self):
        self.abs_moi = self.calc_abs_moi()

    def calc_abs_moi(self):
        abs_moi = np.array([self.moi[0] +  # Parallel axis theorem
                            (self.rel_pos[1] ** 2 + self.rel_pos[2] ** 2)
                            * self.mass,
                            self.moi[1] +
                            (self.rel_pos[0] ** 2 + self.rel_pos[2] ** 2)
                            * self.mass,
                            self.moi[2] +
                            (self.rel_pos[0] ** 2 + self.rel_pos[1] ** 2)
                            * self.mass
                            ])

        return abs_moi


class LiquidFuelTank(Part):
    # TODO: Note to future Max:
    #  1. you gotta find a way to make this Part subclass thing cleaner
    #  2. properly connect this to engine (i.e tanks are parented to engines)
    def __init__(self,
                 name,
                 dry_mass,
                 prop_mass,
                 prop_density,
                 diameter,
                 length,
                 dry_com,
                 rel_pos,
                 rel_rot
                 ):
        # Temporary values
        mass = dry_mass + prop_mass
        com = np.array([0, 0, 0])
        moi = np.array([0, 0, 0])
        # Inherit from Part class
        super().__init__(name,
                         mass,
                         com,
                         rel_pos,
                         moi,
                         rel_rot,
                         )

        self.radius = diameter / 2
        self.length = length

        self.dry_mass = dry_mass
        self.dry_com = dry_com

        self.prop_mass = prop_mass
        self.prop_density = prop_density
        self.prop_com, self.prop_moi = self.calc_fluid()

        self.com = self.calc_com()
        self.moi = self.calc_moi()

    def update_tank(self, mass_flow_rate, dt):
        self.prop_mass -= mass_flow_rate*dt
        self.prop_com, self.prop_moi = self.calc_fluid()
        self.com = self.calc_com()
        self.moi = self.calc_moi()
        self.update_part()

    def calc_fluid(self):
        volume = self.prop_mass/self.prop_density
        height = volume/(np.pi * self.radius**2)
        fluid_com = np.array([0, 0, height/2])
        # Moment of inertia of a cylinder with XY plane at the middle (assuming CoM at middle)
        fluid_moi = np.array([1 / 12 * self.prop_mass * (3 * self.radius**2 + height**2),
                              1 / 12 * self.prop_mass * (3 * self.radius**2 + height**2),
                              1 / 2 * self.prop_mass * self.radius**2
                              ])

        return fluid_com, fluid_moi

    def calc_com(self):
        com = (self.dry_mass * self.dry_com + self.prop_mass * self.prop_com)/self.mass
        return com

    def calc_moi(self):
        # Moment of inertia of a cylindrical shell with XY plane at the middle (assuming CoM at middle)
        dry_moi = np.array([1 / 12 * self.mass * (6 * self.radius**2 + self.length**2),
                            1 / 12 * self.mass * (6 * self.radius**2 + self.length**2),
                            self.mass * self.radius**2
                            ])
        # Parallel axis theorem to align axes for fluid and tank MoI
        prop_abs_moi = np.array([self.prop_moi[0] + self.mass * (self.com[2]-self.prop_com[2])**2,
                                 self.prop_moi[1] + self.mass * (self.com[2]-self.prop_com[2])**2,
                                 self.prop_moi[2]
                                 ])

        return dry_moi + prop_abs_moi


class GaseousFuelTank(Part):

    def __init__(self,
                 name,
                 dry_mass,
                 prop_mass,
                 diameter,
                 length,
                 dry_com,
                 rel_pos,
                 rel_rot
                 ):
        # Temporary values
        mass = dry_mass + prop_mass
        com = np.array([0, 0, 0])
        moi = np.array([0, 0, 0])
        # Inherit from Part class
        super().__init__(name,
                         mass,
                         com,
                         rel_pos,
                         moi,
                         rel_rot,
                         )

        self.radius = diameter / 2
        self.length = length

        self.dry_mass = dry_mass
        self.dry_com = dry_com

        self.prop_mass = prop_mass
        self.prop_com, self.prop_moi = self.calc_fluid()

        self.com = self.calc_com()
        self.moi = self.calc_moi()

    def update_tank(self, mass_flow_rate, dt):
        self.prop_mass -= mass_flow_rate * dt
        self.prop_com, self.prop_moi = self.calc_fluid()
        self.com = self.calc_com()
        self.moi = self.calc_moi()
        self.update_part()

    def calc_fluid(self):
        fluid_com = np.array([0, 0, self.length / 2])
        # Moment of inertia of a cylinder with XY plane at the middle (assuming CoM at middle)
        fluid_moi = np.array([1 / 12 * self.prop_mass * (3 * self.radius ** 2 + self.length ** 2),
                              1 / 12 * self.prop_mass * (3 * self.radius ** 2 + self.length ** 2),
                              1 / 2 * self.prop_mass * self.radius ** 2
                              ])

        return fluid_com, fluid_moi

    def calc_com(self):
        com = (self.dry_mass * self.dry_com + self.prop_mass * self.prop_com) / self.mass
        return com

    def calc_moi(self):
        # Moment of inertia of a cylindrical shell with XY plane at the middle (assuming CoM at middle)
        dry_moi = np.array([1 / 12 * self.mass * (6 * self.radius ** 2 + self.length ** 2),
                            1 / 12 * self.mass * (6 * self.radius ** 2 + self.length ** 2),
                            self.mass * self.radius ** 2
                            ])
        # Parallel axis theorem to align axes for fluid and tank MoI
        prop_abs_moi = np.array([self.prop_moi[0] + self.mass * (self.com[2] - self.prop_com[2]) ** 2,
                                 self.prop_moi[1] + self.mass * (self.com[2] - self.prop_com[2]) ** 2,
                                 self.prop_moi[2]
                                 ])

        return dry_moi + prop_abs_moi


class Engine(Part):

    def __init__(self,
                 name,
                 mass,
                 com,
                 rel_pos,
                 moi,
                 rel_rot,
                 isp,
                 avg_thrust,
                 burn_time,
                 thrust_curve,
                 cot,
                 gimbal,
                 gimbal_limits
                 ):
        # Inherit from Part class
        super().__init__(name,
                         mass,
                         com,
                         rel_pos,
                         moi,
                         rel_rot
                         )
        # Motor Specs
        self.isp = isp
        self.avg_thrust = avg_thrust
        self.burn_time = burn_time
        self.thrust_curve = thrust_curve
        self.cot = cot
        # Thrust
        self.thrust_scalar = self.calc_thrust_scalar(0)
        self.rel_thrust_vec = self.calc_rel_thrust_vector()
        # Mass flow rate
        self.avg_mass_flow_rate = (self.avg_thrust / g_0) / self.isp
        self.mass_flow_rate = self.calc_mass_flow_rate()
        # Gimbal
        self.gimbal = gimbal  # Spherical coordinates
        self.gimbal_limits = gimbal_limits  # Spherical coordinates

    def update_engine(self, t):
        self.update_part()
        self.thrust_scalar = self.calc_thrust_scalar(t)
        self.rel_thrust_vec = self.calc_rel_thrust_vector()
        self.mass_flow_rate = self.calc_mass_flow_rate()

    def calc_thrust_scalar(self, t):
        if t >= 0:
            x, y = self.thrust_curve
            thrust = np.interp(t, x, y)
        else:
            thrust = 0

        return thrust

    def calc_rel_thrust_vector(self):
        """
        Returns thrust vector in the rocket frame of reference.
        """
        # Convert from spherical coordinates to cartesian coordinates
        # All angles must be in radians
        theta, phi = self.gimbal + self.rel_rot
        vec = np.array([self.thrust_scalar * np.sin(theta) * np.cos(phi),
                        self.thrust_scalar * np.sin(theta) * np.sin(phi),
                        self.thrust_scalar * np.cos(theta)
                        ])

        return vec

    def calc_mass_flow_rate(self):
        mass_flow_rate = (self.thrust_scalar / g_0) / self.isp

        return mass_flow_rate

    def gimbal_engine(self, spherical_coords, t):
        self.gimbal = np.clip(spherical_coords,
                              self.gimbal_limits[0],
                              self.gimbal_limits[1]
                              )
        self.update_engine(t)


class SolidMotor(Engine):

    def __init__(self,
                 name,
                 delay,
                 diameter,
                 length,
                 mass,
                 prop_mass,
                 avg_thrust,
                 burn_time,
                 thrust_curve,
                 cot,
                 com,
                 rel_pos,
                 rel_rot,
                 gimbal,
                 gimbal_limits
                 ):
        # Temporary values
        isp = 0
        moi = np.array([0, 0, 0])
        # Inherit from Engine class
        super().__init__(name,
                         mass,
                         com,
                         rel_pos,
                         moi,
                         rel_rot,
                         isp,
                         avg_thrust,
                         burn_time,
                         thrust_curve,
                         cot,
                         gimbal,
                         gimbal_limits
                         )
        self.delay = delay
        self.radius = diameter / 2
        self.length = length
        self.prop_mass = prop_mass
        self.initial_prop_mass = self.prop_mass
        prop_volume = np.pi * self.radius**2 * self.length
        self.prop_density = self.prop_mass/prop_volume
        self.isp = (self.avg_thrust/g_0)/(self.prop_mass/self.burn_time)
        self.moi = self.calc_moi()

    def update_solid_motor(self, t, step):
        self.update_engine(t - self.delay)
        self.prop_mass -= self.mass_flow_rate * step
        self.mass -= self.mass_flow_rate * step
        self.moi = self.calc_moi()
        self.update_part()

    def calc_moi(self):
        delta_m = self.initial_prop_mass - self.prop_mass  # Lost mass
        bore_radius = np.sqrt(delta_m / (self.prop_density*self.length*np.pi))
        # Moment of inertia of a thick-walled cylindrical tube with XY plane at the middle (assuming CoM at middle)
        moi = np.array([1 / 12 * self.mass * (3 * (self.radius**2 + bore_radius**2) + self.length**2),
                        1 / 12 * self.mass * (3 * (self.radius**2 + bore_radius**2) + self.length**2),
                        1 / 2 * self.mass * (self.radius**2 + bore_radius**2)
                        ])

        return moi


class HybridEngine(Engine):

    def __init__(self,
                 name,
                 delay,
                 diameter,
                 length,
                 mass,
                 prop_mass,
                 avg_thrust,
                 burn_time,
                 thrust_curve,
                 cot,
                 com,
                 rel_pos,
                 rel_rot,
                 gimbal,
                 gimbal_limits
                 ):
        # Temporary init
        isp = 0
        moi = np.array([0, 0, 0])
        # Inherit from Engine class
        super().__init__(name,
                         mass,
                         com,
                         rel_pos,
                         moi,
                         rel_rot,
                         isp,
                         avg_thrust,
                         burn_time,
                         thrust_curve,
                         cot,
                         gimbal,
                         gimbal_limits
                         )
        self.delay = delay
        self.radius = diameter / 2
        self.length = length
        self.prop_mass = prop_mass
        self.initial_prop_mass = self.prop_mass
        prop_volume = np.pi * self.radius**2 * self.length
        self.prop_density = self.prop_mass/prop_volume
        self.isp = (self.avg_thrust/g_0)/(self.prop_mass/self.burn_time)
        self.moi = self.calc_moi()

    def update_solid_motor(self, t, step):
        self.update_engine(t - self.delay)
        self.prop_mass -= self.mass_flow_rate * step
        self.mass -= self.mass_flow_rate * step
        self.moi = self.calc_moi()
        self.update_part()

    def calc_moi(self):
        delta_m = self.initial_prop_mass - self.prop_mass  # Lost mass
        bore_radius = np.sqrt(delta_m / (self.prop_density*self.length*np.pi))
        # Moment of inertia of a thick-walled cylindrical tube with XY plane at the middle (assuming CoM at middle)
        moi = np.array([1 / 12 * self.mass * (3 * (self.radius**2 + bore_radius**2) + self.length**2),
                        1 / 12 * self.mass * (3 * (self.radius**2 + bore_radius**2) + self.length**2),
                        1 / 2 * self.mass * (self.radius**2 + bore_radius**2)
                        ])

        return moi


class LiquidEngine(Engine):

    def __init__(self,
                 name,
                 isp,
                 avg_thrust,
                 burn_time,
                 thrust_curve,
                 cot,
                 com,
                 mass,
                 rel_pos,
                 moi,
                 rel_rot,
                 gimbal,
                 gimbal_limits
                 ):
        # Inherit from Engine class
        super().__init__(name,
                         mass,
                         com,
                         rel_pos,
                         moi,
                         rel_rot,
                         isp,
                         avg_thrust,
                         burn_time,
                         thrust_curve,
                         cot,
                         gimbal,
                         gimbal_limits
                         )


class Rocket:

    def __init__(self,
                 engines,
                 com,
                 cop,
                 moi,
                 dry_mass,
                 cs_area,
                 cd,
                 pos=np.array([0, 0, 0]),
                 rot=np.array([np.pi/2, 0, 0])
                 ):
        self.engines = engines
        self.dry_com = com
        self.cop = cop
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

        Returns: COM position
        """
        # TODO: this is kinda crap, separate tanks and engines
        engine_masses = np.array([0, 0, 0])
        engine_weighted_position = np.array([0, 0, 0])
        for e in self.engines:
            engine_masses += e.mass
            engine_weighted_position += e.mass * (e.rel_pos + e.com)
        # Calculate COM
        com = (self.dry_com * self.dry_mass + engine_weighted_position) \
            / (self.dry_mass + engine_masses)

        return com

    def calc_mass(self):
        total_mass = self.dry_mass
        for e in self.engines:
            total_mass += e.mass

        return total_mass

    def calc_position(self, dt):
        """
        Calculate rocket position in global frame of ref
        """
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
        # TODO: this is kinda crap, separate tanks and engines
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
        Returns: weight vector.
        """
        weight = self.mass * np.array([0, 0, -g])

        return weight

    def calc_total_thrust(self):
        """
        Returns: thrust vector.
        """
        total_rel_vec = np.array([0, 0, 0])  # Init thrust vector relative to rocket
        for e in self.engines:
            total_rel_vec += e.rel_thrust_vec  # Add all engine thrust vectors

        # Matrix for general 3D rotation
        gamma, beta, alpha = self.rot  # Get rocket orientation
        matrix = np.array([
                            [
                                np.cos(alpha)*np.cos(beta),
                                np.cos(alpha)*np.sin(beta) *
                                np.sin(gamma)-np.sin(alpha)*np.cos(gamma),
                                np.cos(alpha)*np.sin(beta) *
                                np.cos(gamma)+np.sin(alpha)*np.sin(gamma)
                                ],
                            [
                                np.sin(alpha)*np.cos(beta),
                                np.sin(alpha)*np.sin(beta) *
                                np.sin(gamma)+np.cos(alpha)*np.cos(gamma),
                                np.sin(alpha)*np.sin(beta) *
                                np.cos(gamma)-np.cos(alpha)*np.sin(gamma)
                                ],
                            [
                                -np.sin(beta),
                                np.cos(beta)*np.sin(gamma),
                                np.cos(beta)*np.cos(gamma)
                             ]
                           ])
        # Apply rocket rotation (in global frame of ref) to thrust vector (in rocket frame of ref)
        rotation = Rotation.from_matrix(matrix)
        total_thrust = rotation.apply(total_rel_vec)

        return total_thrust

    def calc_drag(self, air_rho):
        """
        Returns: drag vector.
        """
        drag = 0.5 * (air_rho * self.vel ** 2 * self.cd * self.cs_area)

        return drag

    def calc_total_external_force(self):
        """
        Returns: external forces vector.
        """
        total_ext = self.weight + self.total_thrust + self.drag

        return total_ext

    def calc_total_torque(self):
        """
        Returns: total applied torque in the rocket frame of reference.
        """
        total_torque = np.array([0, 0, 0])
        # Torque generated by engines
        for e in self.engines:
            position_vec = self.com - (e.rel_pos + e.cot)
            total_torque += np.cross(position_vec, e.rel_thrust_vec)
        # Torque generated by aerodynamic forces at the CoP
        # Assuming CoP is constant for low AoA (rocket is mostly facing the stream)
        position_vec = self.com - self.cop
        total_torque += np.cross(position_vec, self.drag)

        return total_torque
