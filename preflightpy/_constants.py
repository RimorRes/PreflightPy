g_0 = 9.80665  # Standard gravity (m/s2)
air_molar_mass = 0.02896968  # Air molar mass (kg/mol)
gas_constant = 8.314462618  # Gas constant (J/(K.mol))
air_gamma = 1.4  # Air heat capacity ratio
air_rho_0 = 1.2252  # Standard air density (kg/m3)
earth_radius = 6356766  # Standard Earth radius (m)

hb = [  # Layer base altitudes
        0,
        11000,
        20000,
        32000,
        47000,
        51000,
        71000
]

pb = [  # Layer base pressures
        101325,
        22632.1,
        5474.89,
        868.019,
        110.906,
        66.9389,
        3.95642
]

tb = [  # Layer base temperatures
        288.15,
        216.65,
        216.65,
        228.65,
        270.65,
        270.65,
        214.65
]

lm = [  # Layer lapse rates
        -0.0065,
        0.0,
        0.001,
        0.0028,
        0.0,
        -0.0028,
        -0.002
]
