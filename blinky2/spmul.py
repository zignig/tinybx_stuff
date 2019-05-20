# serial / par multiply


from nmigen import *


class mul(Elaboratable):
    def __init__(self,sig_width=16,coef_width=10):
        self.sig_in = Signal(sig_width)
        self.coef_in = Signal(coef_width)
        self.coef_width = coef_width
        self.start = Signal()
        self.done = Signal()
        self.do_mul = Signal()

        self.result = Signal(sig_width)

        self.accumulator = Signal(coef_width+sig_width)
        self.coef_reg = Signal(coef_width)
        self.sig_reg = Signal(sig_width)

    def elaborate(self,platform):
        m = Module()
        m.d.sync += self.do_mul.eq(0)
        with m.FSM() as fsm:
            for i in range(self.coef_width):
                with m.State('step_'+str(i)):
                    m.d.sync += self.do_mul.eq(1)
                    m.next = 'step_'+str(i+1)
        return m

if __name__ == "__main__":
    import argparse
    from nmigen import cli
    parser = argparse.ArgumentParser()
    cli.main_parser(parser)
    args = parser.parse_args()

    tb = mul()
    ios = (tb.result,tb.done,)

    cli.main_runner(parser,args,tb,name="lsfr",ports=ios)



