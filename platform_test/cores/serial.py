import itertools

from nmigen.build import Resource, Subsignal, Pins
from nmigen.build import ResourceError
from .gizmo import Gizmo, IO

from nmigen import *
from .uart import UART, Loopback


class Serial(Gizmo):
    " Uart connection in 4 registers"

    def build(self):
        serial = self.platform.request("serial", 0)
        print(serial)
        clock = self.platform.lookup("clk16").clock
        uart = UART(serial.tx, serial.rx, clock.frequency, 9600)
        self.add_device(uart)

        tx_status = IO(
            sig_in=uart.TX.tx_ack, sig_out=uart.TX.tx_ready, name="TX status"
        )
        self.add_reg(tx_status)

        tx_data = IO(sig_out=uart.TX.tx_data, name="TX data")
        self.add_reg(tx_data)

        rx_status = IO(
            sig_in=uart.RX.rx_ready, sig_out=uart.RX.rx_ack, name="RX status"
        )
        self.add_reg(rx_status)

        rx_data = IO(sig_in=uart.RX.rx_data, name="RX data")
        self.add_reg(rx_data)


class SerialLoop(Gizmo):
    " Loopback uart on serial 0 and serial 1"

    def build(self):

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
