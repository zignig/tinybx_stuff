"pin object"

from nmigen import *

class Pin:
    def __init__(self,name,pin_name):
        self.name = name
        self.pin_name = pin_name
        self.assigned = False
        self.pin = Signal(name=name)
        self.input = False
        self.tristate = False

    def set_input(self):
        self.input = True

    def pin_mode(self):
        if self.input:
            i = Signal()
            o = Signal()
            oe = Signal()
            return Instance("SB_IO",
                    p_PIN_TYPE=Const(0b0110_01,6),
                    p_PULLUP=Const(0,1),
                    io_PACKAGE_PIN=self.pin,
                    o_D_IN_0=i,
                    )
        elif self.tristate:
            i = Signal()
            o = Signal()
            oe = Signal()
            return Instance("SB_IO",
                    p_PIN_TYPE=Const(0b0110_01,6),
                    p_PULLUP=Const(0,1),
                    io_PACKAGE_PIN=self.pin,
                    o_D_IN_0=i,
                    i_D_OUT_0=o,
                    io_OUTPUT_ENABLE=oe
                    )
        else:
            return

    def __repr__(self):
        return self.name+'-'+self.pin_name+'-'+str(self.assigned)
bxpins = {
    "PIN_1": "A2",
    "PIN_2": "A1",
    "PIN_3": "B1",
    "PIN_4": "C2",
    "PIN_5": "C1",
    "PIN_6": "D2",
    "PIN_7": "D1",
    "PIN_8": "E2",
    "PIN_9": "E1",
    "PIN_10": "G2",
    "PIN_11": "H1",
    "PIN_12": "J1",
    "PIN_13": "H2",
    "PIN_14": "H9",
    "PIN_15": "D9",
    "PIN_16": "D8",
    "PIN_17": "C9",
    "PIN_18": "A9",
    "PIN_19": "B8",
    "PIN_20": "A8",
    "PIN_21": "B7",
    "PIN_22": "A7",
    "PIN_23": "B6",
    "PIN_24": "A6",
    "SPI_SS": "F7",
    "SPI_SCK": "G7",
    "SPI_IO0": "G6",
    "SPI_IO1": "H7",
    "SPI_IO2": "H4",
    "SPI_IO3": "J8",
    "PIN_25": "G1",
    "PIN_26": "J3",
    "PIN_27": "J4",
    "PIN_28": "G9",
    "PIN_29": "J9",
    "PIN_30": "E8",
    "PIN_31": "J2",
    "LED": "B3",
    "USBP": "B4",
    "USBN": "A4",
    "USBPU": "A3",
    "clk": "B2",
}
