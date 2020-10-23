import preflightpy as pre

params = pre.Parameters(engine=[243, 500, 15, [0, 15], [500, 500]],
                        fuel=[0],
                        mass=[10],
                        aero=[0.0556, 0.0255364],
                        env=[113],
                        sim=[0.01]
                        )

print(params)
s = pre.System(params)

for point in s.launch():
    print(point)
