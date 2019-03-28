" Basic framwork for a tinyFGPBx SOC"
import pins

class Pin:
    def __init__(self,name,pin_name):
        self.name = name
        self.pin_name = pin_name
        self.assigned = False

class Device:
    " a device to add to the core "
    def __init__(self):
        pass
        


class BX:
    def __init__(self):
        self.pins = {}
        for i,j in pins.bxpins.items():
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

