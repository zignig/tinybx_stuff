from nmigen import *
from minerva.core import Minerva
from nmigen_boards.tinyfpga_bx import TinyFPGABXPlatform 

class minerva_core(Elaboratable):
    def elaborate(self, platform):
        clk16    = platform.request("clk16", 0)

        m = Module()
        m.domains.sync  = ClockDomain()
        m.d.comb += ClockSignal().eq(clk16.i)
        
        cpu = Minerva(with_icache=False, with_dcache=False, with_muldiv=False)

        m.submodules.minerva = cpu

        return m

if __name__ == "__main__":
    platform = TinyFPGABXPlatform()
    platform.build(minerva_core(),build_dir='minerva')

