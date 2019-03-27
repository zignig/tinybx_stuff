# linear shift feedback register periph

from nmigen import *
from functools import reduce
from operator import xor
import os
from random import randint
#  collection of mls , https://users.ece.cmu.edu/~koopman/lfsr

class lsfr:
    def __init__(self,width=31,taps=[27,30],initial=50):
        self.o = Signal()
        self.width = width
        self.taps = taps
        self.initial = initial

    def elaborate(self,platform):
        m = Module()
        state = Signal(self.width,reset=self.initial)
        m.d.comb += self.o.eq(~reduce(xor,[state[i] for i in self.taps]))
        m.d.sync += Cat(state).eq(Cat(self.o,state))
        return m


def get_taps(mls):
    " takes a hex string and turns it into taps"
    val = int(mls,16)
    bin_string = bin(val)[2:]
    bits = len(bin_string)
    taps = []
    for i,j in enumerate(bin_string):
        if j == '1':
            taps.append(i)
    return bits,taps


def get_lsfr(min_size=1,max_size=50):
    sizes = os.listdir('max_len_seq/')
    taps = []
    for i in sizes:
        if i.endswith('.txt'):
            t = int(i[:-4])
            if (t >= min_size) and (t <= max_size):
                f = open('max_len_seq/'+i)
                li = f.readlines()
                f.close()
                for j in li:
                    taps.append(j)
    select = randint(0,len(taps))
    val = taps[select]
    bits,tap = get_taps(val)
    initial = randint(1,2**bits)
    print(val,bits,tap,initial)
    return lsfr(bits,tap,initial)


if __name__ == "__main__":
    import argparse
    from nmigen import cli
    parser = argparse.ArgumentParser()
    cli.main_parser(parser)
    args = parser.parse_args()

    tb= get_lsfr()
    ios = (tb.o,)

    cli.main_runner(parser,args,tb,name="lsfr",ports=ios)
