from nmigen import * 

import math 

class Sin(Elaboratable):
    def __init__(self,width=16,resolution=16):
        self.table = Memory(width=width,depth=resolution)
        self.resolution = resolution

        # make the sin table
        points = []
        inc = 1.0/resolution
        scale = 2**width
        print(scale)
        for i in range(resolution):
            val = math.sin(2*math.pi*inc*i)
            print(i,val)
            points.append(round(val*scale))
        print(points)
        self.table.init = points

if __name__ == "__main__":
    a = Sin(resolution=32)

