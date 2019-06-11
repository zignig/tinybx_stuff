import itertools

from nmigen.build import Resource, Subsignal, Pins
from nmigen.build import ResourceError
from .gizmo import Gizmo, IO

from nmigen import *


class UserLeds(Gizmo):
    def build(self):
        leds = []
        for n in itertools.count():
            try:
                l = self.platform.request("user_led", n)
                print(l)
                leds.append(l)
            except ResourceError:
                break

        leds = Cat(led.o for led in leds)
        o = IO(sig_out=leds, name="user_leds")
        self.add_reg(o)
