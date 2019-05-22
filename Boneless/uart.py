from nmigen import *
from nmigen.lib.cdc import MultiReg


__all__ = ["RS232RX", "RS232TX"]


class RS232RX(Elaboratable):
    def __init__(self, tuning_word):
        self.rx = Signal()
        self.data = Signal(8)
        self.stb = Signal()
        self.tuning_word = tuning_word

    def elaborate(self, platform):
        m = Module()

        uart_clk_rxen = Signal()
        phase_accumulator_rx = Signal(32)

        rx = Signal()
        m.submodules += MultiReg(self.rx, rx)
        rx_r = Signal()
        rx_reg = Signal(8)
        rx_bitcount = Signal(4)
        rx_busy = Signal()
        rx_done = self.stb
        rx_data = self.data
        m.d.sync += [
            rx_done.eq(0),
            rx_r.eq(rx)
        ]
        with m.If(~rx_busy):
            with m.If(~rx & rx_r):  # look for start bit
                m.d.sync += [
                    rx_busy.eq(1),
                    rx_bitcount.eq(0)
                ]
        with m.Else():
            with m.If(uart_clk_rxen):
                m.d.sync += rx_bitcount.eq(rx_bitcount + 1)
                with m.If(rx_bitcount == 0):
                    with m.If(rx):  # verify start bit
                        m.d.sync += rx_busy.eq(0)
                with m.Elif(rx_bitcount == 9):
                    m.d.sync += rx_busy.eq(0)
                    with m.If(rx):  # verify stop bit
                        m.d.sync += [
                            rx_data.eq(rx_reg),
                            rx_done.eq(1)
                        ]
                with m.Else():
                    m.d.sync += rx_reg.eq(Cat(rx_reg[1:], rx))
        with m.If(rx_busy):
            m.d.sync += Cat(phase_accumulator_rx, uart_clk_rxen).eq(phase_accumulator_rx + self.tuning_word)
        with m.Else():
            m.d.sync += Cat(phase_accumulator_rx, uart_clk_rxen).eq(2**31)

        return m

    def read(self):
        while not (yield self.stb):
            yield
        value = yield self.data
        # clear stb, otherwise multiple calls to this generator keep returning the same value
        yield
        return value


class RS232TX(Elaboratable):
    def __init__(self, tuning_word):
        self.tx = Signal(reset=1)
        self.data = Signal(8)
        self.stb = Signal()
        self.ack = Signal()
        self.tuning_word = tuning_word

    def elaborate(self, platform):
        m = Module()

        uart_clk_txen = Signal()
        phase_accumulator_tx = Signal(32)

        tx_reg = Signal(8)
        tx_bitcount = Signal(4)
        tx_busy = Signal()
        m.d.sync += self.ack.eq(0)
        with m.If(self.stb & ~tx_busy & ~self.ack):
            m.d.sync += [
                tx_reg.eq(self.data),
                tx_bitcount.eq(0),
                tx_busy.eq(1),
                self.tx.eq(0)
            ]
        with m.Elif(uart_clk_txen & tx_busy):
            m.d.sync += tx_bitcount.eq(tx_bitcount + 1)
            with m.If(tx_bitcount == 8):
                m.d.sync += self.tx.eq(1)
            with m.Elif(tx_bitcount == 9):
                m.d.sync += [
                    self.tx.eq(1),
                    tx_busy.eq(0),
                    self.ack.eq(1)
                ]
            with m.Else():
                m.d.sync += [
                    self.tx.eq(tx_reg[0]),
                    tx_reg.eq(Cat(tx_reg[1:], 0))
                ]
        with m.If(tx_busy):
            m.d.sync += Cat(phase_accumulator_tx, uart_clk_txen).eq(phase_accumulator_tx + self.tuning_word)
        with m.Else():
            m.d.sync += Cat(phase_accumulator_tx, uart_clk_txen).eq(0)

        return m

    def write(self, data):
        yield self.stb.eq(1)
        yield self.data.eq(data)
        yield
        while not (yield self.ack):
            yield
        yield self.stb.eq(0)
