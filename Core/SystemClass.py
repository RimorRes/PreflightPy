Oximport math
from Core.ParamsClass import Params

class System:

    def __init__(self, burnTime, step=1, allinfo=False):
        """Runs a rocket launch simulation within the given parameters"""

        """ Storing parameters """

        p = Params()

        # Processing arguments
        self.burnT = burnTime
        self.t = step
        self.allinfo = allinfo

        # Rocket specs
        self.isp, self.f, self.OFratio, self.OxDens, self.FDens, self.TMat, self.strpM, self.Ft0, self.Ft1, self.Oxt0, self.Oxt1, self.Reserve, self.Cd, self.Rr = p.values

        self.Ft = [self.Ft0, self.Ft1]

        self.Oxt = [self.Oxt0, self.Oxt1]

        self.w = self.f/9.81/self.isp
        self.dF = self.w * (1/(self.OFratio+1))
        self.dOx = (self.w - self.dF)

        self.F = (self.dF * self.burnT)/((100 - self.Reserve)/100)
        self.Ox = (self.dOx * self.burnT)/((100 - self.Reserve)/100)

        self.FtM = self.F / (self.FDens * self.Ft[0]**2) * (2 * self.Ft[0] * self.Ft[1] + self.Ft[1]**2) * self.TMat

        self.OxtM = self.Ox / (self.OxDens * self.Oxt[0]**2) * (2 * self.Oxt[0] * self.Oxt[1] + self.Oxt[1]**2) * self.TMat
        self.dryM = self.strpM + self.FtM + self.OxtM

        self.Across = self.Rr**2 * math.pi

        """ Initializing sim variables """

        self.Fd = self.altitude = self.v = self.maxV = self.Mach = self.maxMach = self.maxAcc = self.a = self.time = 0
        self.Vsound = 330

        self.vs = self.acs = self.ts = self.sounds = self.alts = []

        #print("Ox mass:",self.Ox,"\tFuel mass:",self.F,"\tVolumes:",self.Ox/self.OxDens,self.F/self.FDens)

    def genoutput(self,*args):

        self.log = open('Flight.log','a')

        for arg in args:
            self.log.write(arg+' : '+str(round(eval(arg, self.__dict__),5))+'\t')

        self.log.write('\n')
        self.log.close()

    def analysis(self, coast=False):

        if self.allinfo:
            self.genoutput("time","f","m","v","Mach","a","altitude")
            if not coast:
                eval("self.g.progressBar('Accelerating...', s.time, s.burnT, color='green')")
            elif coast:
                eval("self.g.progressBar('Coasting...', s.v, s.maxV, color='yellow')")

        self.ts.append(self.time)
        self.vs.append(self.v)
        self.acs.append(self.a)
        self.sounds.append(self.Vsound)
        self.alts.append(self.altitude)

        self.time += self.t

        #print(self.a,self.Fd,self.v,self.m,self.f)


    def burn(self, tplus):
        """ SCIENCE!!! """
        if tplus == self.burnT:
            return

        self.pre_process()

        self.analysis(coast=True)

        self.post_process()

        self.checks()

        self.altitude += self.getDistance()

        return self.burn(tplus + self.t)

    def coast(self):
        """ PHYSICS!!! """
        if self.v <= 0:
            return

        self.pre_process()

        self.analysis(coast=True)

        self.post_process(coast=True)

        self.checks(coast=True)

        self.altitude += self.getDistance()

        return self.coast()

    def pre_process(self):
        """ Run the pre-process math """
        self.wetM = (self.Ox + self.F)
        self.m = self.wetM + self.dryM

        self.a = (self.f-(self.m * 9.81 + self.Fd))/self.m

    def post_process(self,coast=False):
        """ Run the post-process math """
        self.v += self.a * self.t

        self.Temp = self.getTemp(self.altitude)
        self.Vsound = math.sqrt(1.4*286.9* self.Temp)
        self.Mach = self.v/self.Vsound


        self.AirPres = self.getPressure(self.altitude,self.Temp)
        self.AirDens = self.getDensity(self.AirPres,self.Temp)

        self.Fd = self.AirDens * self.v**2 * self.Cd * self.Across * 0.5

        if not coast:
            self.Ox -= self.dOx * self.t
            self.F -= self.dF * self.t

    def checks(self,coast=False):
        """ Check for any runtime error and run peak value tests """
        #Peak Acceleration test
        if self.a > self.maxAcc:
            self.maxAcc = self.a

        if self.v > self.maxV:
            self.maxV = self.v

        if self.Mach > self.maxMach:
            self.maxMach = self.Mach

        #Error Loop
        if self.Fd + self.m * 9.81 > self.f and not coast:
            raise RuntimeError("TWR below 1 : {0} at T+ {1}".format(self.f/(self.Fd + self.m * 9.81), self.time))

    def getDistance(self):

        return self.v * self.t + (self.a * self.t**2)/2 # Altitude increment

    def getTemp(self,alt : float):
        """ Get the air temperature """
        if alt <= 11000 :
            return 15.04 - 0.00649*alt +273
        elif 11000 < alt <= 25000 :
            return -56.46 +273
        elif alt > 25000 :
            return -131.21 + 0.00299*alt + 273

    def getPressure(self,alt,temp):
        """ Get the air pressure """
        try:
            return 101.325 * math.exp(0 -((0.02896*9.81)/(8.3143* temp))* alt)
        except OverflowError:
            return 0

    def getDensity(self,pressure,temp):
        """ Get the air density """
        return 0.02896 / ((1 * 8.3143 * temp) / (pressure * 1000) )
