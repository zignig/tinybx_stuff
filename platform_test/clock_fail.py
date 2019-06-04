from nmigen import *
from nmigen.vendor.board.tinyfpga_bx import *


class Counter(Elaboratable):
    def __init__(self,width=21):
        self.counter = Signal(width)
        self.width = width 
        self.o = Signal()

    def elaborate(self,platform):
        m = Module()
        m.d.sync += self.counter.eq(self.counter+1)
        m.d.comb += self.o.eq(self.counter[-1])
        return m
        
class Multi(Elaboratable):
    def __init__(self,count=4):
        self.count = count
        self.o = Signal(count)

    def elaborate(self,platform):
        m = Module()
        for i in range(self.count):
            c = Counter()
            m.submodules += c
        
        return m

class Blinky(Elaboratable):
    def elaborate(self, platform):
        clk16   = platform.request("clk16", 0)
        user_led = platform.request("user_led", 0)
        counter  = Signal(22)

        m = Module()
        m.domains.sync = ClockDomain()
        m.d.comb += ClockSignal().eq(clk16.i)
        m.d.sync += counter.eq(counter + 1)
        m.d.comb += user_led.o.eq(counter[-1])

        co = Multi(20)
        m.submodules.counter = co

        return m


if __name__ == "__main__":
    platform = TinyFPGABXPlatform()
    platform.build(Blinky())#, do_program=True)
