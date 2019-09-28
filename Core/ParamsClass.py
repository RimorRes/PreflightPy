class Params:

    def __init__(self):

        file = open("Core/RFTE.params",'r')

        self.values = []

        for i in file.readlines():
            if i[0] == '=':
                continue
            else:
                x = i.split(':')
                self.values.append(float(x[1].strip()))

        file.close()
