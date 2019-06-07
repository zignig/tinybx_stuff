from nmigen import *
from nmigen.cli import main, pysim


# PWM up and down ramping
class Breathe(Elaboratable):
    def __init__(self, width=18, phase=0.0, stretch=200):
        self.width = width

        self.counter = Signal(width)
        self.value = Signal(width, reset=(int(2 ** width) * phase))

        self.enable = Signal(reset=1)

        # Attach this to your led
        self.o = Signal()

        # Some signals for sequencing
        self.top = Signal()
        self.bottom = Signal()

        # UP or DOWN
        self.updown = Signal(reset=1)

        # Increment ramp delay
        self.stretcher = Signal(max=stretch + 1)
        self.stretch = stretch

    def elaborate(self, platform):
        m = Module()
        with m.If(self.enable):
            # PWM
            with m.If(self.counter < self.value):
                m.d.comb += self.o.eq(1)
            with m.Else():
                m.d.comb += self.o.eq(0)

            m.d.sync += self.counter.eq(self.counter + 1)

            # ramp up and down
            m.d.sync += self.stretcher.eq(self.stretcher + 1)
            with m.If(self.stretcher == self.stretch):
                m.d.sync += self.stretcher.eq(0)
                with m.If(self.updown == 1):
                    m.d.sync += self.value.eq(self.value + 1)
                    with m.If(self.value == 2 ** self.width - 2):
                        m.d.sync += self.updown.eq(0)
                        m.d.sync += [self.top.eq(1), self.bottom.eq(0)]
                with m.If(self.updown == 0):
                    m.d.sync += self.value.eq(self.value - 1)
                    with m.If(self.value == 1):
                        m.d.sync += self.updown.eq(1)
                        m.d.sync += [self.top.eq(0), self.bottom.eq(1)]
        with m.Else():
            m.d.comb += self.o.eq(0)

        return m


if __name__ == "__main__":
    b = Breathe(width=5, stretch=5)
    pins = (b.counter, b.value, b.enable, b.o, b.updown, b.top, b.bottom)
    main(b, pins, name="top")
