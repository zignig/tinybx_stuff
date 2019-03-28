from nmigen import *
from nmigen.cli import main, pysim
from .device import Device

class Counter(Device):
    def __init__(self, width):
        self.v = Signal(width, reset=2 ** width - 1)
        self.o = Signal()

    def elaborate(self, platform):
        m = Module()
        m.d.sync += self.v.eq(self.v + 1)
        m.d.comb += self.o.eq(self.v[-1])
        return m
