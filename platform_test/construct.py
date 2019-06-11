import itertools
from nmigen import *
from nmigen_boards.tinyfpga_bx import *
from nmigen.build import Resource, Subsignal, Pins
from nmigen.build import ResourceError
from nmigen.tools import bits_for

from boneless.gateware.core_fsm import BonelessFSMTestbench

from uart import Loopback, UART
from processor import Boneless

from cores.larson import OnOff
from cores.breathe import Breathe

from cores.gizmo import TestGizmo
from cores.user_leds import UserLeds
from cores.serial import Serial
from cores.counter import Counter


class Loop(Elaboratable):
    " Loopback uart on serial 0 and serial 1"

    def __init__(self, baud_rate=9600):
        self.baud_rate = baud_rate

    def elaborate(self, platform):
        clk16 = platform.request("clk16", 0)

        m = Module()
        m.domains.sync = ClockDomain()
        m.d.comb += ClockSignal().eq(clk16.i)

        clock = platform.lookup("clk16").clock
        serial = platform.request("serial", 0)
        l = Loopback(serial.tx, serial.rx, clock.frequency, self.baud_rate)
        m.submodules.loopback = l

        serial2 = platform.request("serial", 1)
        l2 = Loopback(serial2.tx, serial2.rx, clock.frequency, 9600)
        m.submodules.loop2 = l2

        return m


class CPU(Elaboratable):
    def elaborate(self, platform):
        clk16 = platform.request("clk16", 0)

        m = Module()
        m.domains.sync = ClockDomain()
        m.d.comb += ClockSignal().eq(clk16.i)

        # Create the serial port
        # clock = platform.lookup("clk16").clock
        # serial = platform.request("serial", 0)
        # debug_uart = UART(serial.tx, serial.rx, clock.frequency, 57600)
        debug_uart = None

        b = Boneless(debug_uart)
        m.submodules.boneless = b

        # Attach two test gizmos
        # tg = TestGizmo("test_gizmo")
        # b.add_gizmo(tg)

        # tg2 = TestGizmo("test_gizmo_2")
        # b.add_gizmo(tg2)

        l = UserLeds("Leds", platform=platform)
        b.add_gizmo(l)
        s = Serial("seial_port", platform=platform)
        b.add_gizmo(s)

        c = Counter("counter1", platform=platform)
        b.add_gizmo(c)
        c2 = Counter("counter2", platform=platform)
        b.add_gizmo(c2)
        # TODO remove following if the gizmotron works

        # Attach the blinky
        # leds = []
        # for n in itertools.count():
        #    try:
        #        leds.append(platform.request("user_led", n))
        #    except ResourceError:
        #        break
        #
        #        leds = Cat(led.o for led in leds)
        # m.d.comb += leds.eq(b.pins)
        #        m.d.comb += leds[0].eq(b.pins)
        #        m.d.comb += leds[1].eq(debug_uart.TX.tx_ready)
        #        m.d.comb += leds[2].eq(debug_uart.TX.tx_ack)

        return m


if __name__ == "__main__":
    from plat import BB

    platform = BB()
    platform.build(CPU(), do_program=True)
