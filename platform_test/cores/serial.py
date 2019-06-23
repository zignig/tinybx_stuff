import itertools

from nmigen.build import Resource, Subsignal, Pins
from nmigen.build import ResourceError
from .gizmo import Gizmo, IO, BIT

from nmigen import *
from .uart import UART, Loopback
from .other_uart import UART as newUART


class Serial(Gizmo):
    " Uart connection in 4 registers"

    def build(self):
        serial = self.platform.request("serial", self.number)
        print(serial)
        clock = self.platform.lookup("clk16").clock
        uart = newUART(serial.tx, serial.rx, clock.frequency, self.baud)
        self.add_device(uart)

        # RX status and data
        rx_status = IO(sig_in=uart.rx.stb, name="rx_status")
        rx_status.add_bit(BIT("stb", 0))
        self.add_reg(rx_status)

        rx_data = IO(sig_in=uart.rx.data, name="rx_data")

        # TX status and data
        self.add_reg(rx_data)
        tx_status = IO(sig_in=uart.tx.ack, sig_out=uart.tx.stb, name="tx_status")
        tx_status.add_bit(BIT("ack", 0))
        tx_status.add_bit(BIT("stb", 0))
        self.add_reg(tx_status)

        tx_data = IO(sig_out=uart.tx.data[0:7], name="tx_data")
        self.add_reg(tx_data)



class OldSerial(Gizmo):
    " Uart connection in 4 registers"

    def build(self):
        serial = self.platform.request("serial", self.number)
        print(serial)
        clock = self.platform.lookup("clk16").clock
        uart = UART(serial.tx, serial.rx, clock.frequency, self.baud)
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

        rx_data = IO(sig_in=uart.RX.rx_data[0:7], name="RX data")
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
