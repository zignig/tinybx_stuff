from boneless.arch.instr import *
from boneless.gateware.core_fsm import BonelessCoreFSM, _ExternalPort
from boneless.assembler.asm import Assembler
from nmigen import *
from nmigen.back import pysim
from nmigen.cli import main


class Boneless:
    def __init__(self, has_pins=False, asmfile="asm/echo.asm"):
        self.memory = Memory(width=16, depth=512)
        self.ext_port = _ExternalPort()
        self.pins = Signal(16, name="pins") if has_pins else None

        #self.usb_in_control = Signal(16,name="usb_in_control")
        #self.usb_in_data = Signal(16,name="usb_in_data")
        #self.usb_out_control = Signal(16,name="usb_out_control")
        #self.usb_out_data = Signal(16,name="usb_out_data")

        self.usbout = Signal(16,name="usbout")
        self.usbin = Signal(16,name="usbin")
        #self.to_host = Signal(16,name="from_host")

        code = Assembler(file_name=asmfile)
        code.assemble()
        self.memory.init = code.code

    def elaborate(self, platform):
        m = Module()

        if self.pins is not None:
            # blinky on port address 0
            with m.If(self.ext_port.addr == 0):
                with m.If(self.ext_port.r_en):
                    m.d.sync += self.ext_port.r_data.eq(self.pins)
                with m.If(self.ext_port.w_en):
                    m.d.sync += self.pins.eq(self.ext_port.w_data)

            with m.If(self.ext_port.addr == 1):
                with m.If(self.ext_port.r_en):
                    m.d.sync += self.ext_port.r_data.eq(self.usbin)
#                with m.If(self.ext_port.w_en):
#                   m.d.sync += self.usbout.eq(self.ext_port.w_data)

#            m.d.sync += self.to_host.eq(1)

#            m.d.comb += self.to_host.eq(5)
#            m.d.comb += self.from_host.eq(5)
#            m.d.sync += self.ext_port.r_data.eq(self.from_host)
#            m.d.sync += self.to_host.eq(self.ext_port.w_data)


#            # usb control data
#            with m.If(self.ext_port.addr == 256):
#                with m.If(self.ext_port.r_en):
#                   m.d.sync += self.ext_port.r_data.eq(self.usb_out_control)
#            # usb data
#            with m.If(self.ext_port.addr == 255):
#                with m.If(self.ext_port.r_en):
#                    m.d.sync += self.ext_port.r_data.eq(self.usb_out_data)
#            # usb control data
#            with m.If(self.ext_port.addr == 254):
#                with m.If(self.ext_port.w_en):
#                    m.d.sync += self.usb_in_control.eq(self.ext_port.w_data)
#            # usb data
#            with m.If(self.ext_port.addr == 253):
#                with m.If(self.ext_port.w_en):
#                    m.d.sync += self.usb_in_data.eq(self.ext_port.w_data)

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

    tb= Boneless(has_pins=True)
    ios = (tb.pins,tb.usbout,tb.usbin)

    cli.main_runner(parser,args,tb,name="boneless_core",ports=ios)
