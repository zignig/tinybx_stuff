from boneless.arch.instr import *
from boneless.gateware.core_fsm import BonelessCoreFSM, _ExternalPort
from boneless.assembler.asm import Assembler
from nmigen import *
from nmigen.back import pysim
from nmigen.cli import main

from nmigen.lib.fifo import SyncFIFO

from uart_base import u

class Buffer:
    " fifo bound to the valid/ready signals "
    def __init__(self,valid,ready,data,width=8,depth=5):
        self.fifo= SyncFIFO(width=width,depth=depth)
        self.valid = valid
        self.ready = ready
        self.data = data

    def elaborate(self,platform):
        m = Module()
        m.submodules.fifo  = self.fifo
        m.d.comb += self.fifo.replace.eq(0)
        m.d.sync += self.ready.eq(self.fifo.writable)
        m.d.sync += self.fifo.we.eq(self.valid)
        m.d.sync += self.fifo.din.eq(self.data)
        return m

class Loopback:
    " testing for pumping serial back"
    def __init__(self,uiv,uir,uid,uov,uor,uod,leds):
        self.uiv = uiv
        self.uir = uir
        self.uid = uid

        self.uov = uov
        self.uor = uor
        self.uod = uod
        self.leds = leds


#//      Directions for the uart
#//    // uart pipeline in (out of the device, into the host)
#//    input [7:0] uart_in_data,
#//    input       uart_in_valid,
#//    output      uart_in_ready,
#//
#//    // uart pipeline out (into the device, out of the host)
#//    output [7:0] uart_out_data,
#//    output       uart_out_valid,
#//    input        uart_out_ready,

    def elaborate(self,platform):
        m = Module()
        data = Signal(8)
        ready = Signal()
        valid = Signal()

        m.d.sync += self.leds[0].eq(ready)
        m.d.sync += data.eq(self.uid)
        m.d.sync += valid.eq(self.uov)
        m.d.sync += ready.eq(self.uir)

        m.d.sync += self.uiv.eq(valid)
        m.d.sync += self.uov.eq(valid)
        m.d.sync += self.uor.eq(ready)
        m.d.sync += self.uod.eq(data)
        return m

class Boneless(Elaboratable):
    def __init__(self, has_pins=False, asmfile="asm/echo.asm"):
        self.memory = Memory(width=16, depth=32)
        self.ext_port = _ExternalPort()
        self.pins = Signal(16, name="pins") if has_pins else None
        # uart interface
        # usb interface
        self.uart = u(9600)
        # fifo signals
        self.usb_in_valid = Signal()
        self.usb_in_ready = Signal()
        self.usb_in_data = Signal(8,name="usb_in_data")


        self.usb_out_valid = Signal()
        self.usb_out_ready = Signal()
        self.usb_out_data = Signal(8,name="usb_out_data")

        #self.in_buffer = Buffer(self.usb_in_valid,self.usb_in_ready,self.usb_in_data)
        #self.out_buffer = Buffer(self.usb_out_valid,self.usb_out_ready,self.usb_out_data)
        self.loopback = Loopback(self.usb_in_valid,self.usb_in_ready,self.usb_in_data,self.usb_out_valid,self.usb_out_ready,self.usb_out_data,self.pins)
        # Code
        code = Assembler(file_name=asmfile)
        code.assemble()
        self.memory.init = code.code

    def elaborate(self, platform):
        m = Module()

        m.submodules.uart = self.uart
        if self.pins is not None:
            # blinky on port address 0
            with m.If(self.ext_port.addr == 0):
                with m.If(self.ext_port.r_en):
                    m.d.sync += self.ext_port.r_data.eq(self.pins)
                with m.If(self.ext_port.w_en):
                    m.d.sync += self.pins.eq(self.ext_port.w_data)

            with m.If(sefl.ext_port.addrr == 0):
                with m.If(self.ex_port.r_en):
                    m.d.sync += self.uart.tx.eq(1)
        #m.submodules.loopback = self.loopback

#        with m.If(self.ext_port.addr == 1):
#            with m.If(self.ext_port.r_en):
#                m.d.sync += self.in_buffer.fifo.we.eq(1)
#                m.d.sync += self.ext_port.r_data.eq(self.in_buffer.fifo.din)
#            with m.If(self.ext_port.w_en):
#                m.d.sync += self.out_buffer.fifo.din.eq(self.ext_port.w_data)
#
#        m.d.sync += self.pins[0].eq(self.out_buffer.fifo.we)

#        m.submodules.in_buffer = self.in_buffer
#        m.submodules.out_buffer = self.out_buffer

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
    ios = (tb.pins,tb.usb_in_data,tb.usb_out_data,tb.usb_in_valid,tb.usb_in_ready,tb.usb_out_valid,tb.usb_out_ready)

    cli.main_runner(parser,args,tb,name="boneless_core",ports=ios)
