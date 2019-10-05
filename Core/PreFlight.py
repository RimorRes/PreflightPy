#!/usr/bin/env python3.7
""" Rocket Flight Telemetry Emulator """

import math
import getopt
import platform
import os
import time


if platform.system() == "Windows":
    SYS_CLR = 'cls'
else:
    SYS_CLR = 'clear'

os.system(SYS_CLR)


class System:
    def __init__(self, burnTime, p, step=1, allinfo=False):
        if not type(p) is dict:
            raise TypeError("Argument `params` is of the wrong type: '{}' instead of 'dict'".format(type(p)))

        # Burn Time
        self.burnT = burnTime

        # Engine specs
        self.isp = float(p['Isp'])
        self.f   = float(p['Thrust'])

        # Fuel specs
        self.OFratio = float(p['FuelMixtureRatio'])

        self.OxDens  = float(p['OxidizerDensity'])
        self.FDens   = float(p['FuelDensity'])

        #self.OxMW = p['OxidizerMolarMass']
        #self.FMW = p['FuelMolarMass']

        self.TMat  = float(p['TankMaterialDensity'])

        # Rocket Mass specs
        self.strpM = float(p['StrippedMass'])

        self.Ft0   = float(p['FuelTankRadius'])
        self.Ft1   = float(p['FuelTankThickness'])
        self.Ft    = [self.Ft0, self.Ft1]

        self.Oxt0  = float(p['OxygenTankRadius'])
        self.Oxt1  = float(p['OxygenTankThickness'])
        self.Oxt   = [self.Oxt0, self.Oxt1]

        self.Reserve = float(p['FuelReservePercentage'])

        # Rocket Body specs
        self.Cd = float(p['DragCoef'])
        self.Rr = float(p['RocketRadius'])

        self.w   = self.f/9.81/self.isp
        self.dF  = self.w * (1/(self.OFratio+1))
        self.dOx = (self.w - self.dF)

        self.F  = (self.dF * self.burnT)/((100 - self.Reserve)/100)
        self.Ox = (self.dOx * self.burnT)/((100 - self.Reserve)/100)

        self.FtM  = self.F / self.FDens / (self.Ft[0]**2 * math.pi) * (((self.Ft[0]+self.Ft[1])**2 - self.Ft[0]**2) * math.pi) * self.TMat
        self.OxtM = self.Ox / self.OxDens / (self.Oxt[0]**2 * math.pi) * (((self.Oxt[0]+self.Oxt[1])**2 - self.Oxt[0]**2) * math.pi) * self.TMat
        self.dryM = self.strpM + self.FtM + self.OxtM

        self.Across = self.Rr**2 * math.pi

        self.t = step

        self.allinfo = allinfo

        #print("Ox mass:",self.Ox,"\tFuel mass:",self.F,"\tVolumes:",self.Ox/self.OxDens,self.F/self.FDens)


    def genoutput(self, *args, tab=False):
        self.log = open('RFTE.log', 'a')
        if tab:
            for arg in args:
                self.log.write("\t"+arg+' : '+str(round(eval(arg, self.__dict__),5))+'\t')
        else:
            for arg in args:
                self.log.write(arg+' : '+str(round(eval(arg, self.__dict__),5))+'\t')

        self.log.write('\n')
        self.log.close()


    def suicideBurn(self):
        """Run a suicide burn simulation, will affct ascent simulation."""
        while self.v > 0 :
            pass


    def run(self):
        """Runs a simulation within the given parameters."""
        
        ## Accelaration phase
        self.Fd = 0
        self.altitude = 0
        self.v = 0
        self.maxV = 0
        self.Mach = 0
        self.maxMach = 0
        self.maxAcc = 0
        self.a = 0
        self.Vsound = 330
        self.time = 0

        self.vs = []
        self.acs = []
        self.ts = []
        self.sounds = []
        self.alts = []

        for i in range(int(self.burnT/self.t)):
            self.calcMass()
            self.calcAcc()

            self.addData()

            if self.allinfo:
                progressBar(i,"Accelerating",int(self.burnT/self.t))
                self.genoutput("time","f","m","v","Mach","a","altitude",tab = True)

            self.setAltitude()
            self.calcSpeed()
            self.calcDrag()
            self.removeFuel()

            self.checks("up")

        self.f = 0
        self.maxV = self.v
        self.maxMach = self.Mach

        ## Deceleration phase
        if self.allinfo:
            print("\n")

        while self.v > 0:
            self.calcMass()
            self.calcAcc()

            self.addData()

            if self.allinfo:
                progressBar(int(self.v),"Decelerating")
                self.genoutput("time","f","m","v","Mach","a","altitude",tab=True)

            self.setAltitude()

            self.calcSpeed()
            self.calcDrag()

            self.checks("down")

        if self.allinfo:
            self.genoutput("time","f","m","v","Mach","a","altitude",tab=True)

        #print(self.altitude)


    def setAltitude(self):
        self.altitude += self.v * self.t + (self.a * self.t**2)/2 # Altitude increment


    def calcMass(self,surplusTime=0):
        self.wetM = (self.Ox + self.F)

        self.m = self.wetM + self.dryM


    def calcAcc(self):
        self.a = (self.f-(self.m * 9.81 + self.Fd))/self.m


    def addData(self):
        self.ts.append(self.time)
        self.vs.append(self.v)
        self.acs.append(self.a)
        self.sounds.append(self.Vsound)
        self.alts.append(self.altitude)

        self.time += self.t

        #print(self.a,self.Fd,self.v,self.m,self.f)


    def calcSpeed(self):
        self.v += self.a * self.t

        self.Temp = self.getTemp(self.altitude)

        self.Vsound = math.sqrt(1.4*286.9* self.Temp)

        self.Mach = self.v/self.Vsound


    def calcDrag(self):
        self.Temp = self.getTemp(self.altitude)

        self.AirPres = self.getPressure(self.altitude,self.Temp)

        self.AirDens = self.getDensity(self.AirPres,self.Temp)

        self.Fd = self.AirDens * self.v**2 * self.Cd * self.Across * 0.5


    def removeFuel(self):
        self.Ox -= self.dOx * self.t
        self.F -= self.dF * self.t


    def checks(self,phase):
        #Peak Acceleration test
        if self.a > self.maxAcc:
            self.maxAcc = self.a

        #Error Loop
        if phase == "up":
            if self.Fd + self.m * 9.81 > self.f:
                raise RuntimeError("TWR below 1 : {}".format(self.f/(self.Fd + self.m * 9.81)))
            else:
                pass


    def getTemp(self,alt):
        if alt <= 11000 :
            return 15.04 - 0.00649*alt +273
        elif 11000 < alt <= 25000 :
            return -56.46 +273
        elif alt > 25000 :
            return -131.21 + 0.00299*alt + 273
        else:
            raise TypeError("Argument `alt` is of the wrong type : '{}' instead of 'int' or 'float'".format(type(alt)))


    def getPressure(self,alt,temp):
        try:
            return 101.325 * math.exp(0 -((0.02896*9.81)/(8.3143* temp))* alt)
        except OverflowError:
            return 0

    def getDensity(self,pressure,temp):
        return 0.02896 / ((1 * 8.3143 * temp) / (pressure * 1000) )


class Params:
    def __init__(self):
        self.f = open("RFTE.params", 'r')
        self.key = ''
        self.value = ''

        self.dict = {}

        for i in self.f.readlines():
            if i[0] == '=':
                continue
            f = i.split(':')
            self.key, self.value = f

            self.key = self.key.strip()
            self.value = self.value.strip()

            #print(self.key, self.value)

            self.dict[self.key] = self.value

        self.f.close()


    def retrieve(self):
        return self.dict


def progressBar( num, msg, percentage = False ):
    """Displays a progress bar. If the bar should represent a percentage, set percentage to the maximum value."""
    if percentage:
        print("\033[1;32;40m" + msg + "... [{0}] {1}".format(u'\u2593' * int(num/percentage*50)+ u'\u2591'* int(50-(num/percentage*50)), str(int(num/percentage*100)) + "%    ") , end="\r\033[0;37;40m")
    else:
        print("\033[1;33;40m" + msg + "... [{0}]".format(u'\u2593' * (num%50)+ u'\u2591'*(50-(num%50))), end="\r\033[0;37;40m")


def Welcome():
    print("==============================================================")
    print("Welcome to the rocket flight telemetry emulator PreFlight!")
    print("==============================================================\n")
    print("\t\t\tNew & Improved!\n")
    print("\t\t\tVersion 2.2.0!")
    print("\n\n\tTo run a command type it then hit ENTER\n\tHelp is provided after entering the command 'help'\n\n")
    

class Console:
    """ Let's the user use 'terminal-like' inputs. """

    def __init__(self):
        self.helpwords = [
                "run(['run','-h'])",
                "clear(['clear','-h'])"
                ]
        self.keywords  = {
                'help'  :'self.help()',
                'quit'  :'quit()',
                'run'   :'self.run({})',
                'clear' :'self.clear({})'
                }

    def read(self):
        cmd = input("-")

        # Formatting the input
        cmd = cmd.replace("\n","").expandtabs().split(" ")
        
        if cmd[0] == 'q' or cmd == 'quit':
            print('Exiting the simulator...')
            time.sleep(1)
            os.system(SYS_CLR)
            print('Bye!')
            quit()
            
        
        argv = [x for x in cmd if not x ==""]

        for i in self.keywords:
            if i in cmd[0]:
                eval(self.keywords[i].format(argv))


    def help(self):
        for cmd in self.helpwords:
            eval('self.' + cmd)


    def clear(self, argv):
        opts, args = getopt.getopt(argv[1:], 'h', ['help'])
        
        for opt, arg in opts:
            if opt in ('-h','--help'):
                print("\nclear: clear")
                print("\n\tClears the console")
                print("\n")
                return

        os.system(SYS_CLR)


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
    -g : draws various graphs. Only available in single analysis mode.\n""")
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
        params = Params()

        #open("RFTE.log", "w").close()

        #print(bool(time))

        if bool(time) == False:
            while True:
                burn_time += 1

                s = System(burn_time,params.retrieve(),step=step,allinfo=info)
                s.run()

                if s.altitude < prevalt:
                    break
                prevalt = s.altitude

                #print(s.altitude)
                progressBar(burn_time,"Testing")

                s.genoutput("burnT","altitude","maxAcc","maxV","maxMach")

            print("\n")
            
        elif bool(time) == True:
            burn_time = time

            log = open("RFTE.log","a")
            log.write("\n// burn : {} s /////////////////////////////////////\n\n".format(burn_time))
            log.close()

            s = System(burn_time, params.retrieve(), step=step, allinfo=info)
            s.run()

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


Welcome()

c = Console()

while True:
    c.read()
