from nmigen import *
from nmigen_boards.tinyfpga_bx import *
from nmigen.build import Resource,Subsignal,Pins

from boneless.gateware.core_fsm import BonelessFSMTestbench 

from uart import Loopback 
from processor import Boneless


class Loop(Elaboratable):
    def elaborate(self, platform):
        clk16    = platform.request("clk16", 0)
        user_led = platform.request("user_led", 0)
        counter  = Signal(23)

        m = Module()
        m.domains.sync = ClockDomain()
        m.d.comb += ClockSignal().eq(clk16.i)
        m.d.sync += counter.eq(counter + 1)
        m.d.comb += user_led.o.eq(counter[-1])

        serial = platform.request("serial",0)
        l = Loopback(serial.tx,serial.rx)
        m.submodules.loopback = l

        serial2  = platform.request("serial",1)
        l2 = Loopback(serial2.tx,serial2.rx)
        m.submodules.loop2 = l2 

        b = Boneless()
        m.submodules.boneless = b
        return m


class CPU (Elaboratable):
    def elaborate(self, platform):
        clk16    = platform.request("clk16", 0)
        user_led = platform.request("user_led", 0)

        m = Module()
        m.domains.sync  = ClockDomain()
        m.d.comb += ClockSignal().eq(clk16.i)

        #counter  = Signal(23)
        #m.d.sync += counter.eq(counter + 1)
        #m.d.comb += user_led.o.eq(counter[-1])

        b = BonelessFSMTestbench() 

        m.submodules.boneless = b
        return m
    
class Extend(TinyFPGABXPlatform):
        resources = TinyFPGABXPlatform.resources + [
        # FTDI link back to pc
            Resource("serial",0,
                Subsignal("tx", Pins("19",conn=("gpio",0),dir="o")),
                Subsignal("rx", Pins("20",conn=("gpio",0),dir="i")),
            ),
        # Serial to AVR
            Resource("serial",1,
                Subsignal("tx", Pins("14",conn=("gpio",0), dir="o")),
                Subsignal("rx", Pins("15",conn=("gpio",0), dir="i")),
            ),
        ]

if __name__ == "__main__":
    platform = Extend()
    platform.build(CPU(), do_program=True)
