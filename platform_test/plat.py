from nmigen import *
from nmigen_boards.tinyfpga_bx import *
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

class BB(TinyFPGABXPlatform):
        resources = TinyFPGABXPlatform.resources + [
        # FTDI link back to pc
            Resource("serial",0,
                Subsignal("tx", Pins("19",conn=("gpio",0),dir="o")),
                Subsignal("rx", Pins("20",conn=("gpio",0),dir="i")),
            ),
            Resource("user_led",1,Pins("12",conn=("gpio",0), dir="o")),
            Resource("user_led",2,Pins("13",conn=("gpio",0), dir="o")),
            Resource("user_led",3,Pins("14",conn=("gpio",0), dir="o")),
            Resource("user_led",4,Pins("15",conn=("gpio",0), dir="o")),
        ]

        clock = 'clk16'
        
        def freq(self):
            clk = self.lookup(self.clock)
            return clk.clock.frequency
