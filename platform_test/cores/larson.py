from nmigen import * 
from nmigen.cli import main, pysim

class Larson(Elaboratable):
    def __init__(self,width=5,stretch=10):
        # width of the scanner
        self.width = width
        self.enable = Signal(reset=1)
        self.track = Signal(width+2,reset=1)
        self.stretcher = Signal(max=stretch)
        self.stretch = stretch
        self.updown = Signal(reset=1)

    def elaborate(self,platform):
        m = Module()
        with m.If(self.enable):
            m.d.sync += self.stretcher.eq(self.stretcher + 1)
            with m.If(self.stretcher == self.stretch):
                m.d.sync +=  self.stretcher.eq(0)
                with m.If(self.updown):
                    with m.If(self.track[self.width+1] == 1):
                        #m.d.sync += self.track[0].eq(1)
                        m.d.sync += self.updown.eq(0)
                    with m.Else():
                        m.d.sync +=  self.track.eq(self.track << 1) 
                with m.If(~self.updown):
                    with m.If(self.track[0] == 1):
                        m.d.sync += self.updown.eq(1)
                    with m.Else():
                        m.d.sync += self.track.eq(self.track >> 1)

        return m
        
if __name__ == "__main__":
    b = Larson(width=4,stretch=50)
    pins = (b.track,b.stretcher,b.stretch,b.updown)
    main(b,pins,name="top")
