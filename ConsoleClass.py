#!/usr/bin/env python3.7

""" Rocket Flight Telemetry Emulator """

import math, getopt, platform, os
import Core.SystemClass as sys

#if platform.system() == "Windows":
    #os.system("cls")
#else:
    #os.system("clear")

class Graphics:

    def welcome(self,version):
        print("==============================================================")
        print("Welcome to the rocket flight telemetry emulator PreFlight !")
        print("==============================================================\n")
        print("\t\t\t New & Improved !\n")
        print("\t\t Current version : v{}!".format(version))
        print("\n\n\tTo run a command type it then hit ENTER\n\tHelp is provided after entering the command 'help'\n\n")

    def progressBar(self, msg, num, ceil, length=50, color="white"):
        """Displays a progress bar. If the bar should represent a percentage, set percentage to the maximum value."""
        theme = "\033[0;37;40m"
        red = "\033[1;31;40m"
        green = "\033[1;32;40m"
        yellow = "\033[1;33;40m"
        blue = "\033[1;34;40m"
        magenta = "\033[1;35;40m"
        cyan = "\033[1;36;40m"
        white = theme

        block = u'\u2593'
        space = u'\u2591'

        percentage = int(num/ceil * length)

        color = eval(color)
        print(color + msg + "... [{0}] {1}".format(block*percentage + space*(length-percentage),
                                                        "{}%".format( str(int(num/ceil*100))).ljust(3) ) , end="\r" + theme)

class Console:
    """ Let's the user use 'terminal-like' inputs. """

    def __init__(self,graphics):

        self.g = graphics

        self.g.welcome("3.0.0")

        self.helpwords = ["run(['run','-h'])","clear(['clear','-h'])"]
        self.keywords = {'help':'self.help()','quit':'quit()','run':'self.run({})','clear':'self.clear({})'}

    def read(self):

        cmd = input()

        # Formatting the input

        cmd = cmd.replace("\n","")
        cmd = cmd.expandtabs()

        cmd = cmd.split(" ")

        argv = [x for x in cmd if not x ==""]

        for i in self.keywords:
            if i in cmd[0]:
                eval(self.keywords[i].format( argv ) )

    def help(self):
        for cmd in self.helpwords:
            eval('self.' + cmd)

    def clear(self,argv):
        opts, args = getopt.getopt(argv[1:], 'h', ['help'])

        for opt, arg in opts:
            if opt in ('-h','--help'):
                print("\nclear: clear")
                print("\n\tClears the console")
                print("\n")
                return

        if platform.system() == "Windows":
            os.system("cls")
        else:
            os.system("clear")

    def run(self,argv):

        opts, args = getopt.getopt(argv[1:], 'ghilos:t:', ['graph','help','info','land','optim','step=','time='])

        opts.sort()

        info = land = optim = time = graph = False
        step = 1

        for opt, arg in opts:

            #print("did this:",opt,arg)

            if opt in ("-g", "--graph"):
                graph = True

            elif opt in ('-h', '--help'):
                print('\nrun: run [-t time] [-s interval]  [-o] [-l] [-i] [-g]')
                print("""\n\tRuns a simulation according to the given options and using the parameters given in RFTE.params
        Creates a log in RFTE.log
        By the default, the command logs the results of each simulation until it reaches the best one""")
                print("""\n\tOptions: -t : specify a duration in seconds to get a single analysis of that burn time. Activates single analysis mode.
        -s : the step between each analysis in seconds.
        -o : enable for flight optimization.
        -l : enable to take into account suicide burns.
        -i : enable to display more progress bar and receive step by step details in the log. Only available in single analysis mode.
        -g : draws various graphs. Only available in single analysis mode.""")
                print("\n")
                return

            elif opt in ("-i", "--info"):
                info = True

            elif opt in ("-l", "--land"):
                land = True

            elif opt in ("-o", "--optim"):
                optim = True

            elif opt in ("-s", "--step"):
                step = float(arg)

            elif opt in ("-t", "--time"):
                time = int(arg)

        if not time:
            info = False
            graph = False

        #print(info,land,optim,step,time)

        burn_time = prevalt = 0

        open("Flight.log","w").close()

        #print(bool(time))

        if bool(time) == False:

            while True:

                burn_time += 1

                s = sys.System(burn_time, step=step, allinfo=info)

                s.burn(0)
                s.f = 0
                s.coast()

                if s.altitude < prevalt:
                    break

                prevalt = s.altitude

                #print(s.altitude)

                self.g.progressBar("Launching...", s.altitude, 4*10**5, color="cyan")
                s.genoutput("burnT","altitude","maxAcc","maxV","maxMach")

            print("\n")

        elif bool(time) == True:

            burn_time = time

            log = open("Flight.log","a")
            log.write("\n// burn : {} s /////////////////////////////////////\n\n".format(burn_time))
            log.close()

            s = sys.System(burn_time, step=step, allinfo=info)

            s.burn(0)
            s.f = 0
            s.coast()

            #print(s.altitude)
            s.genoutput("burnT","altitude","maxAcc","maxV","maxMach")

            print("\n")

            if graph:
                try:
                    import matplotlib.pyplot as plt

                    plt.figure(1)
                    plt.plot(s.ts, s.vs, 'b-', s.ts, s.sounds, 'r-') #,s.tlist, s.vlist, 'bo')
                    plt.axis([0, max(s.ts)+2, min( [min(s.vs), min(s.sounds)] )-10, max( [max(s.vs), max(s.sounds)] )+10])
                    plt.xlabel("time in s")
                    plt.ylabel("Speed in m/s")
                    plt.title("{} s burn time \n speed of sound: red, speed of projectile: blue".format(s.burnT))
                    plt.grid(True)

                    plt.figure(2)
                    plt.plot(s.ts, s.acs, 'g-') #,s.tlist, s.alist, 'g^')
                    plt.axis([0,max(s.ts)+2.5,min(s.acs)-10,max(s.acs)+10])
                    plt.xlabel("time in s")
                    plt.ylabel("Acceleration in m/s2")
                    plt.title("{} s burn time \n acceleration: green".format(s.burnT))
                    plt.grid(True)

                    plt.figure(3)
                    plt.plot(s.ts, s.alts, 'tab:orange') #,s.tlist, s.alist, 'g^')
                    plt.axis([0,max(s.ts)+2.5,min(s.alts)-50,max(s.alts)+500])
                    plt.xlabel("time in s")
                    plt.ylabel("Altitude in m")
                    plt.title("{} s burn time \n altitude: orange".format(s.burnT))
                    plt.grid(True)

                    plt.show()

                except ImportError:
                    pass

        else:
            print("Whatever... restart the program")

c = Console(Graphics())

while True:
    c.read()
