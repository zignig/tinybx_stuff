from nmigen import *

from plat import STEVE


class Blinky(Elaboratable):
    def elaborate(self, platform):
        clk16   = platform.request("clk16", 0)
        user_led = platform.request("user_led", 0)
        counter  = Signal(22)

        m = Module()
        m.domains.sync = ClockDomain()
        m.d.comb += ClockSignal().eq(clk16.i)
        m.d.sync += counter.eq(counter + 1)
        m.d.comb += user_led.o.eq(counter[-1])
        return m


if __name__ == "__main__":
    platform = STEVE()
    platform.build(Blinky(), do_program=True)
