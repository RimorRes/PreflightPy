from context import preflight
from preflight import params
from preflight import system
from preflight import env

def main():
    p = params.Parameters("input/charm.json")
    pe = p.package[4]
    e = env.Environment( pe[1], pe[2], pe[3], pe[4], pe[5], pe[6] )
    s = system.System(p, e, 15)
    s.launch()
    system.plot(s.burn_time, s.plot_data)

if __name__ == '__main__':
    main()
