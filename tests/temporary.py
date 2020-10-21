import preflightpy as pre

params = pre.Parameters("tests/input/case_liquid.json")

burn_time = 10

s = pre.System(params, {0: 500, 15: 500})

for point in s.launch():
    print(point)

"""
 # Output
        self.logout, self.csvout = p.package[5]

        open(self.logout, "w").close()

        self.field_names = [
            "t",
            "thrust",
            "drag",
            "mass",
            "v",
            "mach",
            "a",
            "altitude",
            "asl",
            "twr",
            "max_v",
            "max_mach",
            "max_acc",
            "min_acc",
            "max_g",
            "min_g"
        ]
        with open(self.csvout, "w", newline="") as f:
            csv_writer = csv.writer(f)
            csv_writer.writerow(self.field_names)
            f.close()
            
# Ouput
    # Used by matplotlib
        self.plot_data = [
            [],  # index:0 time
            [],  # index:1 altitude
            [],  # index:2 velocity
            [],  # index:3 speed of sound
            [],  # index:4 acceleration
            [],  # index:5 jerk
            [],  # index:6 snap
            [],  # index:7 drag
            [],  # index:8 temperature
            [],  # index:9 pressure
            []   # index:10 density
            ]
    def output(self, *args):
        with open(self.logout, 'a') as f:
            for arg in args:
                value = str(round(eval(arg, self.__dict__), 5)).ljust(10)
                f.write('\t' + arg + ' : ' + value + '\t')
            f.write('\n')
            f.close()

        values = []
        for field in self.field_names:
            value = str(round(eval(field, self.__dict__), 5))
            values.append(value)

        with open(self.csvout, "a", newline="") as f:
            csv_writer = csv.writer(f)
            csv_writer.writerow(values)
            f.close()

    def add_data(self):
        self.plot_data[0].append(self.t)
        self.plot_data[1].append(self.altitude)
        self.plot_data[2].append(self.v)
        self.plot_data[3].append(self.c)
        self.plot_data[4].append(self.a)
        self.plot_data[5].append(self.j)
        self.plot_data[6].append(self.s)
        self.plot_data[7].append(self.drag)
        self.output(
            "t",
            "thrust",
            "drag",
            "mass",
            "v",
            "mach",
            "a",
            "altitude",
            "asl",
            "twr"
            )


def plot(burn_time: float, plot_data: list):
    pd = plot_data
    t = burn_time
    plt.figure(1)
    plt.plot(pd[0], pd[1])
    plt.xlabel("time (s)")
    plt.ylabel("Altitude (m)")
    plt.title("{} s burn time".format(t))
    plt.grid(True)

    plt.figure(2)
    plt.plot(pd[0], pd[2], pd[0], pd[3])
    plt.xlabel("time (s)")
    plt.ylabel("Velocity (m/s) (orange: sound, blue: rocket)")
    plt.title("{} s burn time".format(t))
    plt.grid(True)

    plt.figure(3)
    plt.plot(pd[0], pd[4])
    plt.xlabel("time (s)")
    plt.ylabel("Acceleration (m/s2)")
    plt.title("{} s burn time".format(t))
    plt.grid(True)

    plt.figure(4)
    plt.subplot(2, 1, 1)
    plt.plot(pd[0], pd[5])
    plt.ylabel("Jerk (m/s3)")
    plt.title("{} s burn time".format(t))
    plt.grid(True)
    plt.subplot(2, 1, 2)
    plt.plot(pd[0], pd[6], 'r-')
    plt.xlabel("time (s)")
    plt.ylabel("Snap (m/s4)")
    plt.grid(True)

    plt.figure(5)
    plt.plot(pd[0], pd[7])
    plt.xlabel("time (s)")
    plt.ylabel("Drag (N)")
    plt.title("{} s burn time".format(t))
    plt.grid(True)

    plt.show()
"""