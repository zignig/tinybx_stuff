from nmigen import *
from nmigen.cli import main, pysim
from .device import Device

class Button(Device):
    def __init__(self, pin):
        self.b  = Signal()
        self.pin = pin

    def elaborate(self, platform):
        m = Module()
        p = platform.get_pin(self.pin)
        platform.set_input(self.pin)
        m.d.comb += self.b.eq(p)
        return m
