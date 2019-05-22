from nmigen import *
import uart

from nmigen.lib.fifo import SyncFIFO

class u(Elaboratable):
    def __init__(self,baud=9600,depth=32):
        self.baud = baud
        # uart
        self.tx = uart.RS232TX(self.baud)
        self.rx = uart.RS232RX(self.baud)
        # fifos
        self.tx_fifo = SyncFIFO(width=8,depth=depth)
        self.rx_fifo = SyncFIFO(width=8,depth=depth)
        self.char = Signal(self.rx_fifo.level.nbits)

    def elaborate(self,platform):
        m = Module()

        m.submodules.tx = tx = self.tx
        m.submodules.rx = rx = self.rx

        m.submodules.txfifo = tf = self.tx_fifo
        m.submodules.rxfifo = rf = self.rx_fifo

        with m.If(rx.stb):
            m.d.sync += rf.re.eq(1)
            m.d.sync += rf.din.eq(rx.data)
        with m.Else():
            m.d.sync += rf.re.eq(0)
        m.d.comb += self.char.eq(self.rx_fifo.level)
        return m


if __name__ == "__main__":
   from nmigen.cli import main
   ua = u(112500)
   main(ua,ports=(ua.tx.tx,ua.rx.rx,ua.char))

