import itertools

from nmigen.build import Resource, Subsignal, Pins
from nmigen.build import ResourceError
from .gizmo import Gizmo,IO

from nmigen import * 
from .uart import UART


class Serial(Gizmo):
    def build(self):
        serial = self.platform.request("serial", 0)
        print(serial)
        clock = self.platform.lookup("clk16").clock
        uart = UART(serial.tx, serial.rx, clock.frequency, 9600)
        self.add_device(uart)

        tx_status  = IO(sig_in=uart.TX.tx_ack,sig_out=uart.TX.tx_ready,name="TX status")
        self.add_reg(tx_status)

        tx_data = IO(sig_out=uart.TX.tx_data,name="TX data")
        self.add_reg(tx_data)

        rx_status = IO(sig_in=uart.RX.rx_ready,sig_out=uart.RX.rx_ack,name="RX status")
        self.add_reg(rx_status)

        rx_data = IO(sig_in=uart.RX.rx_data,name="RX data")
        self.add_reg(rx_data)
