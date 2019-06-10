from nmigen import *
from minerva.core import Minerva
from plat import BB


class minerva_core(Elaboratable):
    def __init__(self):
        pass

    def elaborate(self, platform):
        clk16    = platform.request("clk16", 0)
        user_led = platform.request("user_led", 1)

        m = Module()
        m.domains.sync  = ClockDomain()
        m.d.comb += ClockSignal().eq(clk16.i)
        
        a = Signal()
        m.d.sync += a.eq(~a)
        m.d.comb += user_led.o.eq(a)

        cpu = Minerva(with_icache=False, with_dcache=False, with_muldiv=False)

        m.submodules.minerva = cpu

        return m

if __name__ == "__main__":
    from plat import BB
    platform = BB()
    platform.build(minerva_core(),do_program=True,build_dir='minerva')

