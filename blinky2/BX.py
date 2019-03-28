" Basic framwork for a tinyFGPBx SOC"


class Pin:
    def __init__(self,name,pin_name):
        self.name = name
        self.pin_name = pin_name
        self.assigned = False

class Device:
    " a device to add to the core "
    def __init__(self):
        pass
        

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

class BX:
    def __init__(self):
        self.pins = {}
        for i,j in bxpins.items():
           self.pins[i] = Pin(i,j)
        self.devices = {}

    def get_pin(self,name):
        if name in self.pins:
            p = self.pins[name]
            print(p)
            return p
        else:
            raise BaseError

                
b = BX()

