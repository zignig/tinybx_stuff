" Basic framwork for a tinyFGPBx SOC"
from .pins import Pin
from nmigen import *
from nmigen.back import verilog
from .status import Status
from .device import Device
from .button import Button
from nmigen.hdl.ir import Fragment





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

    def set_input(self,name):
        if name in self.pins:
            p = self.pins[name]
            p.input = True

    def pcf(self):
        active = []
        for i in self.pins:
            pin = self.pins[i]
            if pin.assigned ==True:
                active.append(pin)
        for i in active:
            print(i.name,i.pin_name)

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
        #TODO
        # internal devices and register that check that
        # that they are connected and have a sane way
        # of binding them

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
        for i in self.plat.pins:
            mode = self.plat.pins[i].pin_mode()
            if mode is not None:
                m.submodules += mode
        return m

if __name__ == "__main__":
    b = BX()
    b.prepare()
    b.info()
    b.build()
