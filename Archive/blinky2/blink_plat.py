from nmigen import *
from nmigen.vendor.tinyfpga_bx import *
from nmigen.build import Resource,Subsignal,Pins

import lsfr

class Blinky(Elaboratable):
    def elaborate(self, platform):
        clk16   = platform.request("clk16", 0)
        user_led = platform.request("user_led", 0)
        user_led1 = platform.request("user_led", 1)

        m = Module()
        m.domains.sync = ClockDomain()
        m.d.comb += ClockSignal().eq(clk16.i)


        blink = lsfr.get_lsfr()
        m.submodules.blinky = blink 
        blink1 = lsfr.get_lsfr()
        m.submodules.blinky1 = blink1 
        m.d.comb += user_led.o.eq(blink.o)
        m.d.comb += user_led1.o.eq(blink1.o)
        return m


class Extend(TinyFPGABXPlatform):
    def extend(self):
        print("EXTEND")
        # FTDI link back to pc
        self.add_resources([
            Resource("serial",0,
                Subsignal("tx", Pins("B8", dir="o")),
                Subsignal("rx", Pins("A8", dir="i")),
            ),
            Resource("serial",1,
                Subsignal("tx", Pins("J1", dir="o")),
                Subsignal("rx", Pins("H2", dir="i")),
            ),
            Resource("user_led", 1, Pins("J1", dir="o"), extras=["IO_STANDARD=SB_LVCMOS33"]),
            Resource("user_led", 2, Pins("H1", dir="o"), extras=["IO_STANDARD=SB_LVCMOS33"]),
            Resource("user_led", 3, Pins("H9", dir="o"), extras=["IO_STANDARD=SB_LVCMOS33"]),
            Resource("user_led", 4, Pins("D9", dir="o"), extras=["IO_STANDARD=SB_LVCMOS33"]),
        ])

if __name__ == "__main__":
    platform = Extend()
    platform.build(Blinky(), do_program=True)
