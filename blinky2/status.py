# status led device

from nmigen import *
from device import Device

class Status(Device):
    def __init__(self,pin):
        super(Device,self).__init__()
        self.o = Signal(name=pin)
        self.pin = pin

    def elaborate(self,platform):
        counter = Signal(32)
        m = Module()
        p = platform.get_pin(self.pin)
        print(p)
        m.d.sync += counter.eq(counter+1)
        m.d.comb += self.o.eq(counter[21])
        return m



