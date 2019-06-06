from nmigen import * 
from nmigen.cli import main, pysim

class Larson(Elaboratable):
    def __init__(self,width=5):
        # width of the scanner
        self.width = width
        self.enable = Signal(reset=1)


    def elaborate(self,platform):
        m = Module()
        with m.If(self.enable):
             
        return m
        
if __name__ == "__main__":
    b = Larson(width=5)
    pins = (b.counter,b.value,b.enable,b.o,b.updown,b.top,b.bottom)
    main(b,pins,name="top")
