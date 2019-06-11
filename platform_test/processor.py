from boneless.arch.instr import *
from boneless.gateware.core_fsm import BonelessCoreFSM, _ExternalPort
from boneless.assembler.asm import Assembler
from nmigen import *
from nmigen.back import pysim
from nmigen.cli import main

from uart import UART
from cores.gizmo import Gizmo


class Boneless(Elaboratable):
    def __init__(self, uart, has_pins=True, asmfile="asm/base.asm"):
        self.memory = Memory(width=16, depth=512)  # max of  8*1024 on the 8k
        self.ext_port = _ExternalPort()
        self.pins = Signal(16, name="pins") if has_pins else None
        self.uart = uart
        self.asmfile = asmfile

        # Gizmos
        self.addr = 0 
        # TODO , gizmoize blinky and uart
        self.gizmos = []

    def add_gizmo(self, giz):
        self.gizmos.append(giz)

    def insert_gizmos(self, m, platform):
        print("INSERT GIZMOS")
        for g in self.gizmos:
            g.attach(self, m, platform)

    def prepare(self):
        # Prepare all the gizmos and map their addresses
        print("Preparing gizmos")
        for g in self.gizmos:
           g.prepare(self)

        # TODO , map registers bits and code fragments from gizmos

        # Code
        code = Assembler(file_name=self.asmfile)
        code.assemble()
        self.memory.init = code.code
        self.devices = []

    def elaborate(self, platform):
        m = Module()

        self.insert_gizmos(m, platform)

        m.submodules.mem_rdport = mem_rdport = self.memory.read_port(transparent=False)
        m.submodules.mem_wrport = mem_wrport = self.memory.write_port()

        m.submodules.core = BonelessCoreFSM(
            reset_addr=8,
            mem_rdport=mem_rdport,
            mem_wrport=mem_wrport,
            ext_port=self.ext_port,
        )
        return m


if __name__ == "__main__":
    import argparse
    from nmigen import cli

    parser = argparse.ArgumentParser()
    cli.main_parser(parser)
    args = parser.parse_args()

    tb = Boneless(has_pins=True)
    ios = ()

    cli.main_runner(parser, args, tb, name="boneless_core", ports=ios)
