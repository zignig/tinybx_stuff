from nmigen import * 
from nmigen.cli import pysim

import math 

class Sin(Elaboratable):
    def __init__(self,width=16,resolution=8):
        self.table = Memory(width=width,depth=2**resolution)
        self.r = self.table.read_port()
        self.o = Signal((width,True))
        self.resolution = resolution

        self.tick = 50
        self.counter = Signal(resolution)
        # make the sin table
        points = []
        inc = 1.0/(2**resolution)
        scale = 2**width
        print(scale)
        for i in range(2**resolution):
            val = math.sin(2*math.pi*inc*i)
            print(i,val)
            points.append(round(val*scale))
        print(points)
        self.table.init = points

    def elaborate(self,platform):
        m = Module()
        m.submodules += self.r
        m.d.sync += self.counter.eq(self.counter+1)
        m.d.comb += self.r.addr.eq(self.counter)
        m.d.sync += self.o.eq(self.r.data)
        return m 
        

def tail():
    for i in range(10000):
        yield 

def runner():
    yield from tail()

if __name__ == "__main__":
    tb  = Sin()
    freq = 9600
    print(dir(tb))
    with pysim.Simulator(
        tb,
        vcd_file=open("trig.vcd", "w"),
        #gtkw_file=open("trig.gtkw", "w"),
        traces=[tb.o,tb.counter],
    ) as sim:
        sim.add_clock(freq)
        sim.add_sync_process(runner())
        sim.run()

