from .gizmo import Gizmo, IO
from nmigen import *


class _pwm(Elaboratable):
    def __init__(self, pin):
        self.counter = Signal(16)
        self.value = Signal(16)
        self.o = Signal()
        self.pin = pin

    def elaborate(self, platform):
        m = Module()
        m.d.sync += self.counter.eq(self.counter + 1)
        with m.If(self.counter < self.value):
            m.d.sync += self.counter.eq(0)
            m.d.comb += self.o.eq(1)
        with m.Else():
            m.d.comb += self.o.eq(0)
        m.d.comb += self.pin.eq(self.o)
        return m


class Pwm(Gizmo):
    def build(self, **kwargs):
        pin = self.platform.request("pwm", 0)
        p = _pwm(pin)
        self.add_device(p)
        s = IO(sig_out=p.value, name="counter")
        self.add_reg(s)
