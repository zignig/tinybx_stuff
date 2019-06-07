from nmigen import *
from nmigen.cli import main, pysim
import lsfr

class Counter(Elaboratable):
    def __init__(self, width):
        self.v = Signal(width, reset=2 ** width - 1)
        self.o = Signal()

    def elaborate(self, platform):
        m = Module()
        m.d.sync += self.v.eq(self.v + 1)
        m.d.comb += self.o.eq(self.v[-1])
        return m


class Blinker(Elaboratable):
    def __init__(self,pin,period):
        self.period = period
        self.pin = Signal(name=pin)


    def elaborate(self,platform):
        m = Module()
        counter = lsfr.get_lsfr() #lsfr.lsfr()
        m.submodules += counter
        m.d.comb += self.pin.eq(counter.o)
        return m

class Multi(Elaboratable):
    def __init__(self,pins):
        self.names= pins.split()
        self.pins = []

    def elaborate(self,platform):
        m = Module()
        m.domains.sync = ClockDomain(name="sync",reset_less=True)
        for i,j in enumerate(self.names):
            b = Blinker(j,31+i)
            m.submodules += b
            self.pins.append(b.pin)
            #m.d.comb += self.pins[i].eq(b.pin)
        return m


#b = Blinker("PIN_13",21)
#b = Blinker("PIN_13",21)
b = Multi("LED PIN_12 PIN_13 PIN_14 PIN_15")

if __name__ == "__main__":
    main(b, ports=b.pins,name="top")
