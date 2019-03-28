" Basic framwork for a tinyFGPBx SOC"
import pins
from nmigen import *
from nmigen.back import verilog
from status import Status
from nmigen.hdl.ir import Fragment

class Pin:
    def __init__(self,name,pin_name):
        self.name = name
        self.pin_name = pin_name
        self.assigned = False

    def __repr__(self):
        return self.name+'-'+self.pin_name+'-'+str(self.assigned)

class Device:
    " a device to add to the core "
    def __init__(self):
        pass



" the platform object"
class BX_plat:
    def __init__(self):
        self.pins = {}
        for i,j in pins.bxpins.items():
           self.pins[i] = Pin(i,j)
        self.devices = []

    def get_pin(self,name):
        if name in self.pins:
            p = self.pins[name]
            print(p)
            return p
        else:
            raise BaseError

    def add_device(self,dev):
        self.devices.append(dev)

    def info(self):
        print('PINS')
        for i in self.pins:
            print(self.pins[i])
        print('DEVICES')
        for i in self.devices:
            print(i)


class BX:
    def __init__(self):
        self.plat = BX_plat()
        self.devices = []
        self.add_device(Status('LED'))
        self.s = Signal(64)

    def add_device(self,dev):
        self.plat.devices.append(dev)

    def build(self):
        frag = Fragment.get(self,self.plat)
        print(verilog.convert(frag))

    def elaborate(self,platform):
        m = Module()
        for i in self.plat.devices:
            m.submodules += i
        return m

b = BX()
b.build()
