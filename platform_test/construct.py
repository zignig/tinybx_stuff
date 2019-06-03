from nmigen import *
from nmigen.vendor.tinyfpga_bx import *
from nmigen.build import Resource,Subsignal,Pins


from uart import Loopback 

class Loop(Elaboratable):
    def elaborate(self, platform):
        clk16    = platform.request("clk16", 0)
        user_led = platform.request("user_led", 0)
        counter  = Signal(20)

        m = Module()
        m.domains.sync = ClockDomain()
        m.d.comb += ClockSignal().eq(clk16.i)
        m.d.sync += counter.eq(counter + 1)
        m.d.comb += user_led.o.eq(counter[-1])

        serial = platform.request("serial",0)
        l = Loopback(serial.tx,serial.rx)
        m.submodules.loopback = l
        return m

class Extend(TinyFPGABXPlatform):
    def extend(self):
        print("EXTEND")
        self.add_resources([
            Resource("serial",0,
                Subsignal("tx", Pins("B8", dir="o")),
                Subsignal("rx", Pins("A8", dir="i")),
        ),
        ])

if __name__ == "__main__":
    platform = Extend()
    platform.build(Loop(), do_program=True)
