import itertools
from nmigen import *
from nmigen_boards.tinyfpga_bx import *
from nmigen.build import Resource, Subsignal, Pins
from nmigen.build import ResourceError
from nmigen.tools import bits_for

from boneless.gateware.core_fsm import BonelessFSMTestbench

from processor import Boneless

# Some blinky testing TODO , gizmoize
from cores.larson import OnOff
from cores.breathe import Breathe

# Working gizmos
from cores.gizmo import TestGizmo
from cores.user_leds import UserLeds
from cores.serial import Serial
from cores.counter import Counter


class CPU(Elaboratable):
    def __init__(self,platform,asm_file="asm/base.asm"):
        b = Boneless(asm_file=asm_file)
        self.b = b
        self.platform = platform

        # TODO gizmo needs **Kwargs , to add extra variables to gizmos

        l = UserLeds("Leds", platform=platform)
        b.add_gizmo(l)

        s = Serial("seial_port", platform=platform)  # should pass baud
        b.add_gizmo(s)

        c = Counter("counter1", platform=platform)
        b.add_gizmo(c)

        c2 = Counter("counter2", platform=platform)
        b.add_gizmo(c2)

        # Assign addresses , get code etch
        # TODO test and fix
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
