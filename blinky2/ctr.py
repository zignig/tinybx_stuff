from nmigen import *
from nmigen.cli import main, pysim


class Pin:
    def __init__(self):
        self.io = Signal()
        self.o = Signal()
        self.oe = Signal()
        self.i = Signal()

    def elaborate(self, platform):
        m = Module()
        p = Instance(
            "SB_IO",
            p_PIN_TYPE=C(0b101001, 6),
            io_PACKAGE_PIN=self.io,
            i_OUTPUT_ENABLE=self.oe,
            i_D_OUT_0=self.o,
            o_D_IN_0=self.i,
        )
        m.submodules += p
        return m


class Counter:
    def __init__(self, width):
        self.v = Signal(width, reset=2 ** width - 1)
        self.o = Signal()

    def elaborate(self, platform):
        m = Module()
        m.d.sync += self.v.eq(self.v + 1)
        m.d.comb += self.o.eq(self.v[-1])
        return m


ctr = Counter(width=16)
p = Pin()
if __name__ == "__main__":
    main(p, ports=[p.o])
