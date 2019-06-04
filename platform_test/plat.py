from nmigen import *
from nmigen.vendor.board.tinyfpga_bx import *
from nmigen.build import Resource,Subsignal,Pins

class STEVE(TinyFPGABXPlatform):
        resources = TinyFPGABXPlatform.resources + [
        # FTDI link back to pc
            Resource("serial",0,
                Subsignal("tx", Pins("19",conn=("gpio",0),dir="o")),
                Subsignal("rx", Pins("20",conn=("gpio",0),dir="i")),
            ),
        # Serial to AVR
            Resource("serial",1,
                Subsignal("tx", Pins("14",conn=("gpio",0), dir="o")),
                Subsignal("rx", Pins("15",conn=("gpio",0), dir="i")),
            ),
        ]
