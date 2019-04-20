from nmigen import *
from nmigen.back import pysim
from nmigen.cli import main

from nmigen.lib.fifo import SyncFIFO


class Loopback:
    " testing for pumping serial back"
    def __init__(self):
        self.uiv = Signal() 
        self.uir = Signal() 
        self.uid = Signal(8) 

        self.uov = Signal()
        self.uor = Signal() 
        self.uod = Signal(8) 
        self.leds = Signal(4) 
    

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
                  
        ready = Signal()
        data  = Signal(8)
        valid = Signal()
   
        m.d.sync += ready.eq(self.uir)
        m.d.sync += self.uid.eq(0)
        m.d.sync += self.uiv.eq(0)

        
        m.d.sync += self.leds[1].eq(valid)
        m.d.sync += self.leds[0].eq(self.uir)
        m.d.sync += self.leds[2].eq(0)
        m.d.sync += self.leds[3].eq(ready)

        m.d.comb += data.eq(self.uod)
        m.d.comb += valid.eq(self.uov)
        m.d.sync += self.uor.eq(1)        
        
        return m


if __name__ == "__main__":
    import argparse
    from nmigen import cli
    parser = argparse.ArgumentParser()
    cli.main_parser(parser)
    args = parser.parse_args()

    tb= Loopback()
    ios = (tb.uid,tb.uod,tb.uiv,tb.uir,tb.uov,tb.uor,tb.leds)

    cli.main_runner(parser,args,tb,name="loopback",ports=ios)
