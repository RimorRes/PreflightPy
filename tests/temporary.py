import preflightpy as pre

params = pre.Parameters("tests/input/case_liquid.json")

burn_time = 10

s = pre.System(params, {0: 500, 15: 500})

for point in s.launch():
    print(point)
