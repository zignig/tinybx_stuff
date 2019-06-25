import itertools
from nmigen import *

from nmigen_boards.tinyfpga_bx import *


class EL(Elaboratable):
    def __init__(self, platform):
        self.platform = platform
        self.counter = Signal(16)

    def elaborate(self, platform):
        clk16 = platform.request("clk16", 0)

        m = Module()
        m.domains.sync = ClockDomain()
        m.d.comb += ClockSignal().eq(clk16.i)
        
        m.d.sync += self.counter.eq(self.counter + 1)
        return m


if __name__ == "__main__":
    import argparse
    from nmigen import cli

    parser = argparse.ArgumentParser()
    cli.main_parser(parser)
    args = parser.parse_args()

    platform = TinyFPGABXPlatform()
    
    tb = EL(platform)
    ios = ()

    cli.main_runner(parser, args, tb,platform=platform,ports=ios)

# python sim_fail.py simulate -c 1000 -v test.py
#Traceback (most recent call last):
#  File "sim_fail.py", line 36, in <module>
#    cli.main_runner(parser, args, tb,platform=platform,ports=ios)
#  File "/usr/local/lib/python3.6/dist-packages/nmigen/cli.py", line 71, in main_runner
#    sim.run_until(args.sync_period * args.sync_clocks, run_passive=True)
#  File "/usr/local/lib/python3.6/dist-packages/nmigen/back/pysim.py", line 802, in run_until
#    if not self.step(run_passive):
#  File "/usr/local/lib/python3.6/dist-packages/nmigen/back/pysim.py", line 786, in step
#    self._run_process(process)
#  File "/usr/local/lib/python3.6/dist-packages/nmigen/back/pysim.py", line 749, in _run_process
#    process.throw(e)
#  File "/usr/local/lib/python3.6/dist-packages/nmigen/back/pysim.py", line 442, in clk_process
#    yield clk.eq(1)
#  File "/usr/local/lib/python3.6/dist-packages/nmigen/back/pysim.py", line 711, in _run_process
#    .format(self._name_process(process), signal))
#ValueError: Process '/usr/local/lib/python3.6/dist-packages/nmigen/back/pysim.py:442' sent a request to set signal '(sig clk)', which is a part of combinatorial assignment in simulation

