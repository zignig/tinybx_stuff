from nmigen import *
import uart


class u(Elaboratable):
    def __init__(self,baud):
        self.baud = baud
        self.tx = uart.RS232TX(self.baud)
        self.rx = uart.RS232RX(self.baud) 

    def elaborate(self,platform):
        m = Module()
        m.submodules.tx = tx = self.tx 
        m.submodules.rx = rx = self.rx 
        return m


if __name__ == "__main__":
   from nmigen.cli import main 
   ua = u(112500)
   main(ua,ports=(ua.tx.tx,ua.rx.rx))

