import itertools
from nmigen import *

from processor import Boneless

# Working gizmos
from cores.gizmo import TestGizmo
from cores.user_leds import UserLeds
from cores.serial import Serial
from cores.counter import Counter
from cores.pwm import Pwm


class CPU(Elaboratable):
    def __init__(self, platform, asm_file="asm/base.asm"):
        b = Boneless(asm_file=asm_file)
        self.b = b
        self.platform = platform

        # TODO gizmo needs **Kwargs , to add extra variables to gizmos

        l = UserLeds("leds", platform=platform)
        b.add_gizmo(l)

        s = Serial(
            "serial_port", platform=platform, number=0, baud=9600
        )  # should pass baud
        b.add_gizmo(s)

        c = Counter("counter1", platform=platform)
        b.add_gizmo(c)

        c2 = Counter("counter2", platform=platform)
        b.add_gizmo(c2)

        # p = Pwm("pwm",platform=platform,pin=12)
        # b.add_gizmo(p)

        # Assign addresses , get code etch
        # TODO test and fix
        # TODO integrate assembler
        self.b.prepare()

    def elaborate(self, platform):
        clk16 = platform.request("clk16", 0)

        m = Module()
        m.domains.sync = ClockDomain()
        m.d.comb += ClockSignal().eq(clk16.i)

        m.submodules.boneless = self.b
        return m


if __name__ == "__main__":
    from plat import BB

    platform = BB()
    cpu = CPU(platform)
    platform.build(cpu, do_program=True)
