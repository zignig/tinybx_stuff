from nmigen import * 
from nmigen.cli import main, pysim

class Breathe(Elaboratable):
    def __init__(self,freq,width=16):
        self.width = width
        self.inc = 1

        self.counter = Signal(width)
        self.value = Signal(width)
        
        self.enable = Signal(reset=1)
        self.o = Signal()

        self.top = Signal()
        self.bottom = Signal()

        self.updown = Signal(reset=1)
        self.ramp = Signal(width)
        self.stretch = Signal(5)

    def elaborate(self,platform):
        m = Module()
        with m.If(self.enable):
            # PWM
            with m.If(self.counter < self.value):
                m.d.comb += self.o.eq(1)
            with m.Else():
                m.d.comb += self.o.eq(0)
            m.d.sync += self.counter.eq(self.counter + 1)

            # ramp up and down
            m.d.sync += self.stretch.eq(self.stretch + 1)
            with m.If(self.stretch == 0):
                with m.If(self.updown == 1):
                    m.d.sync += self.value.eq(self.value + self.inc)
                    with m.If(self.value == 2**self.width-2):
                        m.d.sync += self.updown.eq(0)
                with m.If(self.updown == 0):
                    m.d.sync += self.value.eq(self.value - self.inc)
                    with m.If(self.value == 1):
                        m.d.sync += self.updown.eq(1)

        return m
        
if __name__ == "__main__":
    b = Breathe(1000,width=5)
    pins = (b.counter,b.value,b.enable,b.o,b.updown)
    main(b,pins,name="top")
