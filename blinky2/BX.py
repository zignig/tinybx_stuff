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
        self.pin = Signal(name=name)

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
            p.assigned = True
            return p.pin
        else:
            raise BaseError

    def active_pins(self):
        active = []
        for i in self.pins:
            pin = self.pins[i]
            if pin.assigned ==True:
                active.append(pin.pin)
        return active

    def add_device(self,dev):
        self.devices.append(dev)

    def info(self):
        print('PINS')
        print(self.active_pins())
        print('DEVICES')
        for i in self.devices:
            print(i)


class BX:
    def __init__(self):
        self.plat = BX_plat()
        self.add_device(Status('LED'))
        self.add_device(Status('PIN_12'))
        self.add_device(Status('PIN_13'))
        self.add_device(Status('PIN_14'))
        self.add_device(Status('PIN_15'))
        self.s = Signal(64)

    def add_device(self,dev):
        self.plat.devices.append(dev)

    def info(self):
        self.plat.info()

    def prepare(self):
        " build the fragment to assign pins"
        Fragment.get(self,self.plat)

    def build(self):
        frag = Fragment.get(self,self.plat)
        print(verilog.convert(frag,name='top',ports=self.plat.active_pins()))

    def elaborate(self,platform):
        m = Module()
        # TODO auto hook up the pins
        for i in self.plat.devices:
            m.submodules += i
        return m

b = BX()
b.prepare()
b.info()
b.build()
