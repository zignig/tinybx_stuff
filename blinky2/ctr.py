from nmigen import *
from nmigen.cli import main, pysim
from lsfr import get_lsfr


class Pin:
    def __init__(self,name):
        self.name=name
        self.io = Signal()
        self.o = Signal(name=name)
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


class Blinker:
    def __init__(self,pin,period):
        self.period = period
        self.pin = Signal(name=pin)


    def elaborate(self,platform):
        m = Module()
        counter = get_lsfr()
        m.submodules += counter
        m.d.comb += self.pin.eq(counter.o)
        return m

class Multi:
    def __init__(self,pins):
        self.names= pins.split()
        self.pins = []

    def elaborate(self,platform):
        m = Module()
        m.domains += ClockDomain(name="sync",reset_less=True)
        for i,j in enumerate(self.names):
            b = Blinker(j,21+i)
            m.submodules += b
            self.pins.append(Signal(name=j))
            m.d.comb += self.pins[i].eq(b.pin)
        return m


#b = Blinker("PIN_13",21)
#b = Blinker("PIN_13",21)
b = Multi("LED PIN_12 PIN_13 PIN_14 PIN_15")

if __name__ == "__main__":
    main(b, ports=b.pins,name="top")
