# Gizmos auto attach to a the boneless IO
from nmigen import *
from collections import OrderedDict

# TODO gizmos need register maps and bit maps
# that add their names into the assembler setup
# rework address map so it can pre cacluate

class _GizmoCollection:
    def __init__(self):
        object.__setattr__(self,"_modules",OrderedDict())

    def __iadd__(self, modules):
        for module in modules:
            self._modules[module] = module
        return self

    def __setattr__(self, name, submodule):
        self._modules[name] = submodule

    def __setitem__(self, name, value):
        return self.__setattr__(name, value)


class BIT:
    " create a named bit register"

    def __init__(self, name, pos):
        self.name = name
        self.pos = pos


class IO:
    " define and bind a read write register"

    def __init__(self, sig_in=None, sig_out=None, name=None):
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
        return str(self.sig_in) + "--" + str(self.sig_out)


class Gizmo:
    def __init__(self, name, platform=None):
        self.platform = platform
        self.name = name
        self.registers = []
        self.devices = []
        self.code = ""  # assembly code for the gizmo TODO , auto attach
        self.addr = -1
        self.build()

    def build(self):
        print("OVERRIDE ME")

    def add_device(self, dev):
        self.devices.append(dev)

    def add_reg(self, reg):
        self.registers.append(reg)

    def prepare(self,boneless):
        print("Preparing "+str(self.name)+" within "+str(boneless))
        print(self.registers)
        print(self.devices)
        print("----")

    def attach(self, boneless, m, platform):
        print("<< " + self.name + " >>")
        if len(self.registers) > 0:
            for reg in self.registers:
                with m.If(boneless.ext_port.addr == boneless.addr):
                    self.addr = int(boneless.addr)
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
                    # TODO , map the addresses and make it so you can hard set
                    # addresses and the gizmotron with map around them.
                    boneless.addr += 1
                    print()
                    print(self)
        if len(self.devices) > 0:
            for dev in self.devices:
                print(dev)
                m.submodules += dev

    def __repr__(self):
        return "<" + self.name + "|" + str(self.addr) + "|" + str(self.registers) + ">"


class TestGizmo(Gizmo):
    "Test Gizmo"
    code = "NOP"

    def build(self):
        r = IO(Signal(), Signal())
        self.add_reg(r)
        r = IO(Signal(), Signal())
        self.add_reg(r)

# Fake classes for testing
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
    a = _GizmoCollection()
    print("Activate the Gizmotron")
    tg = TestGizmo("test")
    m = Module()
    b = FakeBoneless()
    tg.attach(b, m, None)
