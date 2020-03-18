from nmigen import *
from nmigen.cli import pysim
from nmigen.back.pysim import Tick
from nmigen.hdl.rec import Layout

# Does not hit the "BOUNCE" state if the m.next = "NEXT" is hanging
# second example has an m.Else() and it works as I expected


class FSM_weird(Elaboratable):
    def __init__(self):
        self.counter = Signal(4)
        self.max = 10

    def elaborate(self, platform):
        m = Module()

        # increment the counter
        m.d.sync += self.counter.eq(self.counter + 1)

        with m.FSM() as fsm:
            with m.State("IDLE"):
                with m.If(self.counter == self.max):
                    m.next = "BOUNCE"
                m.next = "NEXT"
                # with a hanging next the BOUNCE state is not executed

            with m.State("NEXT"):
                m.next = "IDLE"

            with m.State("BOUNCE"):
                m.d.sync += self.counter.eq(0)
                m.next = "IDLE"

        return m


class FSM_working(Elaboratable):
    def __init__(self):
        self.counter = Signal(4)
        self.max = 10

    def elaborate(self, platform):
        m = Module()

        # increment the counter
        m.d.sync += self.counter.eq(self.counter + 1)

        with m.FSM() as fsm:
            with m.State("IDLE"):
                with m.If(self.counter == self.max):
                    m.next = "BOUNCE"
                # if there is an m.Else , the above state works
                with m.Else():
                    m.next = "NEXT"

            with m.State("NEXT"):
                m.next = "IDLE"

            with m.State("BOUNCE"):
                m.d.sync += self.counter.eq(0)
                m.next = "IDLE"

        return m


if __name__ == "__main__":
    fsmw = FSM_weird()
    with pysim.Simulator(fsmw, vcd_file=open("fsm_weird.vcd", "w")) as sim:
        sim.add_clock(10)
        sim.run_until(1000, run_passive=True)

    fsmwo = FSM_working()
    with pysim.Simulator(fsmwo, vcd_file=open("fsm_working.vcd", "w")) as sim:
        sim.add_clock(10)
        sim.run_until(1000, run_passive=True)
