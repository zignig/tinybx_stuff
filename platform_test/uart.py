from nmigen import *

# Simon Kirkby
# obeygiantrobot@gmail.com
# 20190610

# ported to migen from Whitequarks original blog post
# https://lab.whitequark.org/notes/2016-10-18/implementing-an-uart-in-verilog-and-migen/


def _divisor(freq_in, freq_out, max_ppm=None):
    divisor = int(freq_in // freq_out)
    if divisor <= 0:
        raise ArgumentError("output frequency is too high")

    ppm = 1000000 * ((freq_in / divisor) - freq_out) / freq_out
    if max_ppm is not None and ppm > max_ppm:
        raise ArgumentError("output frequency deviation is too high")

    return divisor


class RX(Elaboratable):
    def __init__(self, rx, clk_freq, baud_rate):
        self.rx = rx
        self.rx_data = Signal(8)
        self.rx_ready = Signal()
        self.rx_ack = Signal()
        self.rx_error = Signal()
        self.divisor = _divisor(freq_in=clk_freq, freq_out=baud_rate, max_ppm=50000)

    def elaborate(self, platform):
        m = Module()

        rx_counter = Signal(max=self.divisor)
        rx_strobe = Signal()

        m.d.comb += rx_strobe.eq(rx_counter == 0)
        with m.If(rx_counter == 0):
            m.d.sync += rx_counter.eq(self.divisor - 1)
        with m.Else():
            m.d.sync += rx_counter.eq(rx_counter - 1)

        rx_bitno = Signal(3)

        with m.FSM(reset="IDLE") as fsm:
            with m.State("IDLE"):
                with m.If(self.rx_ack):
                    m.d.sync += self.rx_ready.eq(0)
                with m.If(~self.rx):
                    m.d.sync += rx_counter.eq(self.divisor // 2)
                    m.next = "START"

            with m.State("START"):
                with m.If(rx_strobe):
                    m.next = "DATA"

            with m.State("DATA"):
                with m.If(rx_strobe):
                    m.d.sync += self.rx_data.eq(Cat(self.rx_data[1:8], self.rx))
                    m.d.sync += rx_bitno.eq(rx_bitno + 1)
                    with m.If(rx_bitno == 7):
                        m.next = "STOP"

            with m.State("STOP"):
                with m.If(rx_strobe):
                    with m.If(~self.rx):
                        m.next = "ERROR"
                    with m.Else():
                        m.next = "FULL"

            with m.State("FULL"):
                m.d.sync += self.rx_ready.eq(1)
                with m.If(self.rx_ack):
                    m.next = "IDLE"
                with m.Elif(~self.rx):
                    m.next = "ERROR"

            with m.State("ERROR"):
                m.d.sync += self.rx_error.eq(1)

        return m


class TX(Elaboratable):
    def __init__(self, tx, clk_freq, baud_rate):
        self.tx = tx
        self.tx_data = Signal(8)
        self.tx_ready = Signal()
        self.tx_ack = Signal()
        self.divisor = _divisor(freq_in=clk_freq, freq_out=baud_rate, max_ppm=50000)

    def elaborate(self, platform):
        m = Module()

        tx_counter = Signal(max=self.divisor)
        tx_strobe = Signal()
        m.d.comb += tx_strobe.eq(tx_counter == 0)

        with m.If(tx_counter == 0):
            m.d.sync += tx_counter.eq(self.divisor - 1)
        with m.Else():
            m.d.sync += tx_counter.eq(tx_counter - 1)

        tx_bitno = Signal(3)
        tx_latch = Signal(8)

        with m.FSM(reset="IDLE") as fsm:
            with m.State("IDLE"):
                m.d.sync += self.tx_ack.eq(0)
                with m.If(self.tx_ready):
                    m.d.sync += tx_counter.eq(self.divisor - 1)
                    m.d.sync += tx_latch.eq(self.tx_data)
                    m.next = "START"
                with m.Else():
                    m.d.sync += self.tx.eq(1)

            with m.State("START"):
                with m.If(tx_strobe):
                    m.d.sync += self.tx.eq(0)
                    m.d.sync += self.tx_ack.eq(1)
                    m.next = "DATA"

            with m.State("DATA"):
                with m.If(tx_strobe):
                    m.d.sync += self.tx.eq(tx_latch[0])
                    m.d.sync += tx_latch.eq(Cat(tx_latch[1:8], 0))
                    m.d.sync += tx_bitno.eq(tx_bitno + 1)
                    with m.If(tx_bitno == 7):
                        m.next = "STOP"

            with m.State("STOP"):
                with m.If(tx_strobe):
                    m.d.sync += self.tx.eq(1)
                    m.next = "IDLE"

        return m


class UART(Elaboratable):
    def __init__(self, tx, rx, clk_freq, baud_rate):
        self.TX = TX(tx, clk_freq, baud_rate)
        self.RX = RX(rx, clk_freq, baud_rate)

    def elaborate(self, platform):
        m = Module()
        m.submodules.tx = self.TX
        m.submodules.rx = self.RX
        return m


class _TestPads(Module):
    def __init__(self):
        self.rx = Signal()
        self.tx = Signal()

    def elaborate(self, platform):
        m = Module()
        return m


def _test_rx(rx, dut):
    print("test RX")

    def T():
        yield
        yield
        yield
        yield

    def B(bit):
        yield rx.eq(bit)
        yield from T()

    def S():
        print("START BIT")
        yield from B(0)
        assert (yield dut.rx_error) == 0
        assert (yield dut.rx_ready) == 0

    def D(bit):
        print("DATA BIT ", bit)
        yield from B(bit)
        assert (yield dut.rx_error) == 0
        assert (yield dut.rx_ready) == 0

    def E():
        print("END BIT")
        yield from B(1)
        assert (yield dut.rx_error) == 0

    def O(bits):
        print("OUT")
        yield from S()
        for bit in bits:
            yield from D(bit)
        yield from E()

    def A(octet):
        print("ACKNOWLEDGE")
        yield from T()
        assert (yield dut.rx_data) == octet
        yield dut.rx_ack.eq(1)
        while (yield dut.rx_ready) == 1:
            yield
        yield dut.rx_ack.eq(0)

    def F():
        print("FAIL")
        print(dir(dut))
        yield from T()
        assert (yield dut.rx_error) == 1
        yield rx.eq(1)
        yield
        # yield dut.rst.eq(1)
        yield ResetSignal().eq(1)
        yield
        # yield dut.rx_error.eq(0)
        yield
        yield
        yield
        assert (yield dut.rx_error) == 0

    # bit patterns
    print("Bit patterns\n\n")
    yield from O([1, 0, 1, 0, 1, 0, 1, 0])
    yield from A(0x55)
    yield from O([1, 1, 0, 0, 0, 0, 1, 1])
    yield from A(0xC3)
    yield from O([1, 0, 0, 0, 0, 0, 0, 1])
    yield from A(0x81)
    yield from O([1, 0, 1, 0, 0, 1, 0, 1])
    yield from A(0xA5)
    yield from O([1, 1, 1, 1, 1, 1, 1, 1])
    yield from A(0xFF)
    print("end bit patterns\n\n")

    return
    # framing error
    yield from S()
    for bit in [1, 1, 1, 1, 1, 1, 1, 1]:
        yield from D(bit)
    yield from S()
    yield from F()

    # overflow error
    yield from O([1, 1, 1, 1, 1, 1, 1, 1])
    yield from B(0)
    yield from F()


def _test_tx(tx, dut):
    print("test TX")

    def Th():
        yield
        yield

    def T():
        yield
        yield
        yield
        yield

    def B(bit):
        print("BIT ",bit)
        yield from T()
        assert (yield tx) == bit

    def S(octet):
        assert (yield tx) == 1
        # assert (yield dut.tx_ack) == 1
        yield dut.tx_data.eq(octet)
        yield dut.tx_ready.eq(1)
        while (yield tx) == 1:
            yield
        yield dut.tx_ready.eq(0)
        assert (yield tx) == 0
        # assert (yield dut.tx_ack) == 0
        yield from Th()

    def D(bit):
        # assert (yield dut.tx_ack) == 0
        yield from B(bit)

    def E():
        # assert (yield dut.tx_ack) == 0
        yield from B(1)
        yield from Th()

    def O(octet, bits):
        print("data ",str(octet)," ",str(bits))
        yield from S(octet)
        for bit in bits:
            yield from D(bit)
        yield from E()

    yield from O(0x55, [1, 0, 1, 0, 1, 0, 1, 0])
    yield from O(0x81, [1, 0, 0, 0, 0, 0, 0, 1])
    yield from O(0xFF, [1, 1, 1, 1, 1, 1, 1, 1])
    yield from O(0x00, [0, 0, 0, 0, 0, 0, 0, 0])


def _test(tx, rx, dut):
    yield from _test_rx(rx, dut.RX)
    yield from _test_tx(tx, dut.TX)


class Loopback(Elaboratable):
    def __init__(self, tx, rx, clk_freq, baud_rate=9600, debug=False):
        # leds = Cat([plat.request("user_led") for _ in range(8)])
        # debug = plat.request("debug")
        self.debug = debug
        self.uart = UART(tx, rx, clk_freq=clk_freq, baud_rate=baud_rate)
        self.RX = self.uart.RX
        self.TX = self.uart.TX

    def elaborate(self, platform):
        m = Module()

        m.submodules.uart = self.uart

        empty = Signal(reset=1)
        data = Signal(8)
        rx_strobe = Signal()
        tx_strobe = Signal()

        m.d.comb += [
            rx_strobe.eq(self.uart.RX.rx_ready & empty),
            tx_strobe.eq(self.uart.TX.tx_ack & ~empty),
            self.uart.RX.rx_ack.eq(rx_strobe),
            self.uart.TX.tx_data.eq(data),
            self.uart.TX.tx_ready.eq(tx_strobe),
        ]

        with m.If(rx_strobe):
            m.d.sync += data.eq(self.uart.RX.rx_data), empty.eq(0)
        with m.If(tx_strobe):
            m.d.sync += empty.eq(1)

        if self.debug:
            m.d.comb += [
                leds.eq(self.uart.rx_data),
                debug.eq(
                    Cat(
                        serial.rx,
                        serial.tx,
                        self.uart.rx_strobe,
                        self.uart.tx_strobe,
                        # self.uart.rx_fsm.ongoing("IDLE"),
                        # self.uart.rx_fsm.ongoing("START"),
                        # self.uart.rx_fsm.ongoing("DATA"),
                        # self.uart.rx_fsm.ongoing("STOP"),
                        # self.uart.rx_fsm.ongoing("FULL"),
                        # self.uart.rx_fsm.ongoing("ERROR"),
                        # self.uart.tx_fsm.ongoing("IDLE"),
                        # self.uart.tx_fsm.ongoing("START"),
                        # self.uart.tx_fsm.ongoing("DATA"),
                        # self.uart.tx_fsm.ongoing("STOP"),
                    )
                ),
            ]

        return m


if __name__ == "__main__":
    import sys, argparse
    from nmigen import cli
    from nmigen.cli import pysim

    parser = argparse.ArgumentParser()
    parser.add_argument(
        "type", choices=["uart", "sim", "test", "loopback"], default="uart"
    )

    cli.main_parser(parser)

    args = parser.parse_args()

    tx = Signal()
    rx = Signal(reset=1)

    if args.type == "sim":
        freq = 4800
        tb = UART(tx, rx, clk_freq=freq, baud_rate=1200)
        with pysim.Simulator(
            tb,
            vcd_file=open("ctrl.vcd", "w"),
            gtkw_file=open("ctrl.gtkw", "w"),
            traces=[tx, rx],
        ) as sim:
            sim.add_clock(freq)
            sim.add_sync_process(_test(tx, rx, tb))
            # sim.run_until(100e-6, run_passive=True)
            sim.run()

    if args.type == "uart":
        tb = UART(tx, rx, clk_freq=4800, baud_rate=1200)
        ios = (tx, rx, tb.TX.tx_data, tb.RX.rx_data)
        cli.main_runner(parser, args, tb, name=args.type, ports=ios)

    if args.type == "loopback":
        tb = Loopback(tx, rx)
        ios = (tx, rx)
        cli.main_runner(parser, args, tb, name=args.type, ports=ios)
