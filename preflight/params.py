#!usr/bin/env python3

import json
class Parameters:

    def __init__(self, path = "preflight/case.params"):

        file = open(path,'r')
        extension = path.split(".")[1]

        self.package = []

        if extension == "params":
            subgroup = []

            for line in file.readlines():

                if line[0] == '=':
                    self.package.append(subgroup[:])
                    subgroup.clear()

                else:
                    x = line.split(':')
                    subgroup.append( self.cast( x[1].strip() ) )


        elif extension == "json":
            j = json.load(file)

            for subgroup in j.values():
                self.package.append( [ self.cast(x) for x in subgroup.values() ] )

        file.close()

    def cast(self, x):
        try:
            return float(x)
        except:
            return str(x)

# TEMP: for testing purposes
#p = Params()
#print(p.package, len(str(p.package)), type(p.package[0][1]))
