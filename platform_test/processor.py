from boneless.arch.instr import *
from boneless.gateware.core_fsm import BonelessCoreFSM, _ExternalPort
from boneless.assembler.asm import Assembler
from nmigen import *
from nmigen.back import pysim
from nmigen.cli import main

from uart import UART
from cores.gizmo  import Gizmo

class Boneless(Elaboratable):
    def __init__(self, uart, has_pins=True, asmfile="asm/tx.asm"):
        self.memory = Memory(width=16, depth=512)  # max of  8*1024 on the 8k
        self.ext_port = _ExternalPort()
        self.pins = Signal(16, name="pins") if has_pins else None
        self.uart = uart

        # Code
        code = Assembler(file_name=asmfile)
        code.assemble()
        self.memory.init = code.code
        self.devices = []

        # Gizmos
        self.addr = 5 # ( blinky and uarts are built in )
        # TODO , gizmoize blinky and uart
        self.gizmos = []

    def add_gizmo(self,giz):
        self.gizmos.append(giz)

    def insert_gizmos(self,m,platform):
        print("GIZMOS")
        for i in self.gizmos:
            i.attach(self,m,platform)

    def elaborate(self, platform):
        m = Module()

        # external memory

        if self.pins is not None:
            # blinky on port address 0 (W)
            with m.If(self.ext_port.addr == 0):
                with m.If(self.ext_port.w_en):
                    m.d.sync += self.pins.eq(self.ext_port.w_data)

        # UART TX
        # uart tx status on address 1 (R/W)
        with m.If(self.ext_port.addr == 1):
            with m.If(self.ext_port.r_en):
                m.d.sync += self.ext_port.r_data.eq(self.uart.TX.tx_ack)
            with m.If(self.ext_port.w_en):
                m.d.sync += self.uart.TX.tx_ready.eq(self.ext_port.w_data)

        # uart data on address 2 (W)
        with m.If(self.ext_port.addr == 2):
            with m.If(self.ext_port.w_en):
                m.d.sync += self.uart.TX.tx_data.eq(self.ext_port.w_data[0:7])

        # UART RX
        # uart rx status on address 3 (R/W)
        with m.If(self.ext_port.addr == 3):
            with m.If(self.ext_port.r_en):
                m.d.sync += self.ext_port.r_data.eq(self.uart.RX.rx_ready)
            with m.If(self.ext_port.w_en):
                m.d.sync += self.uart.RX.rx_ack.eq(self.ext_port.w_data)

        # uart rx data on address 4 (W)
        with m.If(self.ext_port.addr == 4):
            with m.If(self.ext_port.r_en):
                m.d.sync += self.ext_port.r_data.eq(self.uart.RX.rx_data)

        self.insert_gizmos(m,platform)

        m.submodules.mem_rdport = mem_rdport = self.memory.read_port(transparent=False)
        m.submodules.mem_wrport = mem_wrport = self.memory.write_port()

        m.submodules.uart = self.uart

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
