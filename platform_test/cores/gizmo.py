# Gizmos auto attach to a the boneless IO
from nmigen import * 

class IO:
    def __init__(self,sig_in=None,sig_out=None,name=None):
        self.sig_in = sig_in
        self.sig_out = sig_out
        if name is not None:
            self.name = name

    def has_input(self):
        if self.sig_in is not None:
            return True
        else:
            return False

    def has_output(self):
        if self.sig_out is not None:
            return True
        else:
            return False

    def __repr__(self):
        return str(self.sig_in)+"--"+str(self.sig_out)

class Gizmo:
    def __init__(self, name):
        self.name = name
        self.registers = []
        self.code = "" # assembly code for the gizmo TODO , auto attach
        self.addr= -1
        self.build()

    def add_reg(self,reg):
        self.registers.append(reg)

    def build(self,device=None):
        print("OVERRIDE ME")

    def attach(self,boneless,m,platform):
        if len(self.registers)> 0:
            for reg in self.registers:
                with m.If(boneless.ext_port.addr == boneless.addr):
                    self.addr = int(boneless.addr)
                    print("Bind in/out to boneless_ext_port data")
                    if reg.has_input():
                        print("Binding Input")
                        print(reg.sig_in)
                        with m.If(boneless.ext_port.r_en):
                            m.d.sync += boneless.ext_port.r_data.eq(reg.sig_in)
                    if reg.has_output():
                        print("Binding Output")
                        print(reg.sig_out)
                        with m.If(boneless.ext_port.w_en):
                            m.d.sync += reg.sig_out.eq(boneless.ext_port.w_data)
                    boneless.addr += 1 
                    print()
                    print(self)

    def __repr__(self):
        return "<"+self.name+"|"+str(self.addr)+"|"+str(self.registers)+">"

class TestGizmo(Gizmo):
    "Test Gizmo"
    def build(self):
        r = IO(Signal(),Signal())
        self.add_reg(r)
        r = IO(Signal(),Signal())
        self.add_reg(r)

class ex_int:
    def __init__(self):
        self.addr = Signal(16) 
        self.r_en = Signal() 
        self.w_en = Signal() 
        self.r_data = Signal(16) 
        self.w_data = Signal(16) 

class FakeBoneless:
    def __init__(self):
        self.ext_port = ex_int()
        self.addr = 0

if __name__ == "__main__":
    print("Activate the Gizmotron")
    tg = TestGizmo("test")
    m = Module()
    b = FakeBoneless()
    tg.attach(b,m,None)


