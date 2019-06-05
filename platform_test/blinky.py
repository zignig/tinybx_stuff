import itertools

from nmigen import *
from nmigen.build import ResourceError
from plat import BB


class Blinky(Elaboratable):
    def elaborate(self, platform):
        m = Module()

        clk = platform.request('clk16')
        m.domains.sync = ClockDomain()
        m.d.comb += ClockSignal().eq(clk.i)

        leds = []
        for n in itertools.count():
            try:
                leds.append(platform.request("user_led", n))
            except ResourceError:
                break
        leds = Cat(led.o for led in leds)

        ctr = Signal(max=int(clk.frequency //2), reset=int(clk.frequency//2) - 1)
        bl = Signal(len(leds))
        m.d.comb += leds.eq(bl)
        with m.If(ctr == 0):
            m.d.sync += ctr.eq(ctr.reset)
            m.d.sync += bl.eq(bl+1)
        with m.Else():
            m.d.sync += ctr.eq(ctr - 1)

        return m


if __name__ == "__main__":
    platform = BB()
    platform.build(Blinky(), do_program=True)
