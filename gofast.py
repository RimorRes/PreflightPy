import preflightpy as pre

params = pre.Parameters("tests/input/gofast.json")  # Collects info about the rocket and environmental conditions etc. from the input file.
env = pre.Environment(params.env_variables) #  The 'Environment' takes care of computing conditions (e.g. atmosphere, gravity) at various altitudes.
burn_time = 10.43  # The burn time of your engine in seconds.
s = pre.System(params, env, burn_time)  # The core of this module, it takes care of the main simulation and the output.

s.launch()  # Blast off! Launches the simulation.

# Output, in .csv and .log forms, is located in the output folder specified in the input file
