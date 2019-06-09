from nmigen import *

from boneless.gateware.core_fsm import BonelessFSMTestbench
from nmigen_boards.tinyfpga_bx import TinyFPGABXPlatform 

class boneless_core(Elaboratable):
    def elaborate(self, platform):
        clk16    = platform.request("clk16", 0)
        user_led = platform.request("user_led", 0)

        m = Module()
        m.domains.sync  = ClockDomain()
        m.d.comb += ClockSignal().eq(clk16.i)
        
        cpu = BonelessFSMTestbench(has_pins=True)

        m.d.sync += user_led.eq(cpu.pins[0])
        m.submodules.cpu = cpu

        return m

if __name__ == "__main__":
    platform = TinyFPGABXPlatform()
    platform.build(boneless_core(),do_program=True,build_dir='boneless')

