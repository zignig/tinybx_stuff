import itertools

from nmigen.build import Resource, Subsignal, Pins
from nmigen.build import ResourceError
from .gizmo import Gizmo, IO, BIT

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

        leds_cat = Cat(led.o for led in leds)
        o = IO(sig_out=leds_cat, name="user")
        for i, j in enumerate(leds):
            o.add_bit(BIT("led_" + str(i), i))
        self.add_reg(o)
