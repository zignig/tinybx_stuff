from .gizmo import Gizmo,IO
from nmigen import * 

class counter(Elaboratable):
    def __init__(self):
        self.counter = Signal(16)

    def elaborate(self,platform):
        m = Module()
        m.d.sync += self.counter.eq(self.counter +1)
        return m


class Counter(Gizmo):
    def build(self):
        c = counter()
        self.add_device(c)
        s = IO(sig_in=c.counter,name="counter")
        self.add_reg(s)


