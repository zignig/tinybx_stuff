from boneless.arch.instr import *
from boneless.gateware.core_fsm import BonelessCoreFSM, _ExternalPort
from boneless.assembler.asm import Assembler

from nmigen import *
from nmigen.back import pysim
from nmigen.cli import main

from cores.gizmo import Gizmo


class Boneless(Elaboratable):
    def __init__(self, asm_file="asm/base.asm"):
        self.memory = Memory(width=16, depth=512)  # max of  8*1024 on the 8k
        self.ext_port = _ExternalPort()
        self.asm_file = asm_file

        # Gizmos
        self.addr = 0
        self.gizmos = []
        self.mapping = {}

    def add_gizmo(self, giz):
        self.gizmos.append(giz)

    def insert_gizmos(self, m, platform):
        print("Insert Gizmos")
        for g in self.gizmos:
            g.attach(self, m, platform)

    def prepare(self):
        # Prepare all the gizmos and map their addresses
        print("Preparing Gizmos")
        for g in self.gizmos:
            g.prepare(self)
        print("Dump gizmo data")
        for g in self.gizmos:
            g.dump()
            print(g.map())
        # TODO , map registers bits and code fragments from gizmos

        # Code
        code = Assembler(file_name=self.asm_file)
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

    tb = Boneless()
    ios = ()

    cli.main_runner(parser, args, tb, name="boneless_core", ports=ios)
