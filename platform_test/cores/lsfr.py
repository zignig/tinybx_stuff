# linear shift feedback register periph

from nmigen import *
from functools import reduce
from operator import xor
import os
from random import randint

#  collection of mls , https://users.ece.cmu.edu/~koopman/lfsr
import mls


class lsfr(Elaboratable):
    def __init__(self, width=31, taps=[27, 30], initial=50, s=1):
        self.o = Signal()
        self.width = width
        self.taps = taps
        self.initial = initial
        self.stretcher = Signal(20)
        self.stretch = s

    def elaborate(self, platform):
        m = Module()
        state = Signal(self.width, reset=self.initial)
        m.d.comb += self.o.eq(~reduce(xor, [state[i] for i in self.taps]))
        with m.If(self.stretcher == self.stretch):
            m.d.sync += Cat(state).eq(Cat(self.o, state))

        with m.If(self.stretcher == self.stretch + 1):
            m.d.sync += self.stretcher.eq(0)
        with m.Else():
            m.d.sync += self.stretcher.eq(self.stretcher + 1)
        return m


def get_taps(mls):
    " takes a hex string and turns it into taps"
    val = int(mls, 16)
    bin_string = bin(val)[2:]
    bits = len(bin_string)
    taps = []
    for i, j in enumerate(reversed(bin_string)):
        if j == "1":
            taps.append(i)
    return bits, taps


def get_lsfr(min=11, max=32):
    taps = []
    for i in mls.seq:
        if (i >= min) and (i <= max):
            for j in mls.seq[i]:
                taps.append(j)
    select = randint(0, len(taps) - 1)
    val = taps[select]
    bits, tap = get_taps(val)
    initial = randint(1, 2 ** bits - 1)
    assert initial != 0
    print(val, bits, tap, initial)
    return lsfr(bits, tap, initial)


if __name__ == "__main__":
    import argparse
    from nmigen import cli

    parser = argparse.ArgumentParser()
    cli.main_parser(parser)
    args = parser.parse_args()

    tb = get_lsfr()
    ios = (tb.o,)

    cli.main_runner(parser, args, tb, name="lsfr", ports=ios)
