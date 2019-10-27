from nmigen import *


class ClockDivisor(Elaboratable):
    " clock divider "
    def __init__(self, factor):
        self.v = Signal(factor)
        self.o = Signal()

    def elaborate(self, platform):
        m = Module()
        m.d.sync += self.v.eq(self.v + 1)
        m.d.comb += self.o.eq(self.v[-1])
        return m
