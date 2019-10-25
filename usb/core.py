from nmigen import *

from lambdausb.cfg import ConfigurationEndpoint
from lambdausb.dev import USBDevice
from lambdausb.lib import stream
from lambdausb.phy.usb import USBPHY
from lambdausb.protocol import Transfer


from nmigen_boards.tinyfpga_bx import *
from pll import PLL

class BlinkerEndpoint(Elaboratable):
    def __init__(self, led):
        self.led = led 
        self.sink = stream.Endpoint([("data", 8)])

    def elaborate(self, platform):
        m = Module()

        led = Signal()
        sel = Signal()

        m.d.comb += self.sink.ready.eq(Const(1))
        with m.If(self.sink.valid):
            m.d.sync += sel.eq(self.sink.data[:1])

        clk_freq = platform.default_clk_frequency
        ctr = Signal.range(int(clk_freq//2), reset=int(clk_freq//2)-1)
        with m.If(ctr == 0):
            m.d.sync += ctr.eq(ctr.reset)
            m.d.sync += led.eq(~led)
        with m.Else():
            m.d.sync += ctr.eq(ctr - 1)

        m.d.comb += [
            self.led.o.eq(sel & led),
        ]

        return m


class USBBlinker(Elaboratable):
    def elaborate(self, platform):
        m = Module()

        # USB device
        usb_phy = m.submodules.ulpi_phy = USBPHY(platform.request("usb", 0),48e6)
        usb_dev  = m.submodules.usb_dev  = USBDevice(usb_phy)

        # Configuration endpoint
        from config import descriptor_map, rom_init
        cfg_ep  = m.submodules.cfg_ep = ConfigurationEndpoint(descriptor_map, rom_init)
        cfg_in  = usb_dev.input_port(0x0, 64, Transfer.CONTROL)
        cfg_out = usb_dev.output_port(0x0, 64, Transfer.CONTROL)

        m.d.comb += [
            cfg_ep.source.connect(cfg_in),
            cfg_out.connect(cfg_ep.sink)
        ]

        # RGB blinker endpoint
        ep  = m.submodules.ep = BlinkerEndpoint(platform.request("led", 0))
        out = usb_dev.output_port(0x1, 512, Transfer.BULK)

        m.d.comb += out.connect(ep.sink)

        return m


class Top(Elaboratable):
    def elaborate(self,platform):
            m = Module()

            clk_pin = platform.request(platform.default_clk,dir="-")

            # PLL
            pll = PLL(16,48)
            m.submodules.pll = pll
            #m.domains.sync = ClockDomain()
            m.domains += pll.domain
            m.d.comb += [
                    pll.clk_pin.eq(clk_pin),
                    ClockSignal().eq(pll.clk_pin)
            ]
            # USB Device
            blinker = USBBlinker()
            m.submodules.usb = blinker

            return m

if __name__ == "__main__":
    platform = TinyFPGABXPlatform()
    t = Top() 
    platform.build(t)
