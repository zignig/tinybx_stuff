from nmigen import *
from nmigen.cli import main, pysim

class OnOff(Elaboratable):
    def __init__(self,stretch=200):
        self.stretcher = Signal(max=stretch+1)
        self.stretch = stretch 
        self.o = Signal()

    def elaborate(self,platform):
        m = Module()
        m.d.sync += self.stretcher.eq(self.stretcher + 1)
        with m.If(self.stretch == self.stretcher):
            m.d.sync += self.stretcher.eq(0)
            m.d.sync += self.o.eq(~self.o)
        return m

# PWM up and down ramping on enable
class Fade(Elaboratable):
    def __init__(self, width=8, stretch=5):
        self.width = width

        self.counter = Signal(width)
        self.value = Signal(width)

        self.enable = Signal(reset=1)
        self.active = Signal()

        # Attach this to your led
        self.o = Signal()

        self.stretcher = Signal(max=stretch + 1)
        self.stretch = stretch

    def elaborate(self, platform):
        m = Module()
        with m.If(self.enable):
            # PWM
            with m.If(self.counter < self.value + 1):
                m.d.comb += self.o.eq(1)
            with m.If(self.counter +1  > self.value):
                m.d.comb += self.o.eq(0)

            m.d.sync += self.counter.eq(self.counter + 1)

            # Fade up on active
            m.d.sync += self.stretcher.eq(self.stretcher + 1)
            with m.If(self.stretcher == self.stretch):
                m.d.sync += self.stretcher.eq(0)
                with m.If(self.active == 1):
                    with m.If(self.value < 2 ** self.width - 1):
                        m.d.sync += self.value.eq(self.value + 1)
                with m.If(self.active == 0):
                    with m.If(self.value > 0):
                        m.d.sync += self.value.eq(self.value - 1)
        with m.Else():
            m.d.comb += self.o.eq(0)

        return m

class Larson(Elaboratable):
    def __init__(self, width=5, stretch=10):
        # width of the scanner
        self.width = width
        self.enable = Signal(reset=1)
        self.track = Signal(width + 2, reset=1)
        self.stretcher = Signal(max=stretch)
        self.stretch = stretch
        self.updown = Signal(reset=1)

    def elaborate(self, platform):
        m = Module()
        with m.If(self.enable):
            m.d.sync += self.stretcher.eq(self.stretcher + 1)
            with m.If(self.stretcher == self.stretch):
                m.d.sync += self.stretcher.eq(0)
                with m.If(self.updown):
                    with m.If(self.track[self.width + 1] == 1):
                        # m.d.sync += self.track[0].eq(1)
                        m.d.sync += self.updown.eq(0)
                    with m.Else():
                        m.d.sync += self.track.eq(self.track << 1)
                with m.If(~self.updown):
                    with m.If(self.track[0] == 1):
                        m.d.sync += self.updown.eq(1)
                    with m.Else():
                        m.d.sync += self.track.eq(self.track >> 1)
        with m.Else():
            m.d.sync += self.track.eq(0)
        return m

class FadeTest(Elaboratable):
    def __init__(self,stretch=500):
        self.o = Signal()
        self.stretch = stretch

    def elaborate(self,platform):
        m = Module() 
        fader = Fade()
        onoff = OnOff(stretch=self.stretch)
        m.d.sync += fader.active.eq(onoff.o)
        m.d.comb += self.o.eq(fader.o)

        m.submodules.fader = fader
        m.submodules.onoff = onoff

        return m

if __name__ == "__main__":
    #b = Larson(width=4, stretch=50)
    #pins = (b.track, b.stretcher, b.stretch, b.updown)
    #main(b, pins, name="top")
    #f = Fade()
    #pins = (f.o,f.active,f.counter,f.value,f.enable)
    #main(f,pins,name="top")
    #c = OnOff(stretch=500)
    #pins = (c.o,c.stretch,c.stretcher)
    #main(c,pins,name="top")
    f = FadeTest(stretch=4000)
    pins = (f.o)
    main(f,pins,name="fader")
