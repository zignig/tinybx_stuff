" Basic framwork for a tinyFGPBx SOC"
from . import pins
from nmigen import *
from nmigen.back import verilog
from .status import Status
from nmigen.hdl.ir import Fragment

class Pin:
    def __init__(self,name,pin_name):
        self.name = name
        self.pin_name = pin_name
        self.assigned = False
        self.pin = Signal(name=name)

    def __repr__(self):
        return self.name+'-'+self.pin_name+'-'+str(self.assigned)

def B(sig):
    i = Signal()
    o = Signal()
    oe = Signal()
    return Instance("SB_IO",
            p_PIN_TYPE=Const(0b0110_01,6),
            p_PULLUP=Const(0,1),
            io_PACKAGE_PIN=sig,
            o_D_IN_0=i,
            i_D_OUT_0=o,
            io_OUTPUT_ENABLE=oe
            )

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
        m.submodules += B(self.plat.pins['LED'].pin)
        m.submodules += B(self.plat.pins['PIN_15'].pin)
        return m

b = BX()
b.prepare()
b.info()
b.build()
