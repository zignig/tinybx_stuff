class Subsignal:
    def __init__(self,name,pins,stan=""):
        self.name = name
        self.pins = pins
        self.stan = stan

class Pins:
    def __init__(self,name_set):
        pass

class IOStandard:
    def __init__(self,stand):
        self.standard = stand
# IOs ----------------------------------------------------------------------------------------------

_io = [
    ("user_led", 0, Pins("B3"), IOStandard("LVCMOS33")),

    ("usb", 0,
        Subsignal("d_p", Pins("B4")),
        Subsignal("d_n", Pins("A4")),
        Subsignal("pullup", Pins("A3")),
        IOStandard("LVCMOS33")
    ),

    ("spiflash", 0,
        Subsignal("cs_n", Pins("F7"), IOStandard("LVCMOS33")),
        Subsignal("clk", Pins("G7"), IOStandard("LVCMOS33")),
        Subsignal("mosi", Pins("G6"), IOStandard("LVCMOS33")),
        Subsignal("miso", Pins("H7"), IOStandard("LVCMOS33")),
        Subsignal("wp", Pins("H4"), IOStandard("LVCMOS33")),
        Subsignal("hold", Pins("J8"), IOStandard("LVCMOS33"))
    ),

    ("spiflash4x", 0,
        Subsignal("cs_n", Pins("F7"), IOStandard("LVCMOS33")),
        Subsignal("clk", Pins("G7"), IOStandard("LVCMOS33")),
        Subsignal("dq", Pins("G6 H7 H4 J8"), IOStandard("LVCMOS33"))
    ),

    ("clk16", 0, Pins("B2"), IOStandard("LVCMOS33"))
]

# Connectors ---------------------------------------------------------------------------------------

_connectors = [
    # A2-H2, Pins 1-13
    # H9-A6, Pins 14-24
    # G1-J2, Pins 25-31
    ("GPIO", "A2 A1 B1 C2 C1 D2 D1 E2 E1 G2 H1 J1 H2 H9 D9 D8 C9 A9 B8 A8 B7 A7 B6 A6"),
    ("EXTRA", "G1 J3 J4 G9 J9 E8 J2")
]

# Default peripherals
serial = [
    ("serial", 0,
        Subsignal("tx", Pins("GPIO:0")),
        Subsignal("rx", Pins("GPIO:1")),
        IOStandard("LVCMOS33")
    )
]

# Platform -----------------------------------------------------------------------------------------

