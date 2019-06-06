import itertools

from nmigen import *
from nmigen.build import ResourceError
from nmigen.tools import bits_for

# PWM up and down ramping
class Breathe(Elaboratable):
    def __init__(self, width=18,phase=0.0,stretch=200):
        self.width = width

        self.counter = Signal(width)
        self.value = Signal(width,reset=(int(2**width)*phase))

        self.enable = Signal(reset=1)

        # Attach this to your led
        self.o = Signal()

        # Some signals for sequencing
        self.top = Signal()
        self.bottom = Signal()

        # UP or DOWN
        self.updown = Signal(reset=1)

        # Increment ramp delay
        self.stretcher = Signal(max=stretch+1)
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


class Blinky(Elaboratable):
    def __init__(self, clk_name):
        self.clk_name = clk_name

    def elaborate(self, platform):
        m = Module()

        clk = platform.request(self.clk_name)
        clk_freq = platform.get_clock_constraint(clk)
        m.domains.sync = ClockDomain()
        m.d.comb += ClockSignal().eq(clk.i)

        leds = []
        for n in itertools.count():
            try:
                leds.append(platform.request("user_led", n))
            except ResourceError:
                break

        del leds[0]
        l = len(leds)
        for i,j  in enumerate(leds):
            print(i/l,j)
            b = Breathe(phase=(i/l),stretch=50)
            m.submodules += b
            m.d.comb += leds[i].o.eq(b.o)

        #leds = Cat(led.o for led in leds)

        #ctr = Signal(max=int(clk_freq//2), reset=int(clk_freq//2) - 1)
        #with m.If(ctr == 0):
        #    m.d.sync += ctr.eq(ctr.reset)
        #    m.d.sync += leds.eq(~leds)
        #with m.Else():
        #    m.d.sync += ctr.eq(ctr - 1)
        return m


def build_and_program(platform_cls, clk_name, **kwargs):
    platform_cls().build(Blinky(clk_name), do_program=True, **kwargs)
