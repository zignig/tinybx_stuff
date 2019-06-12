# Gizmos auto attach to a the boneless IO
from nmigen import *
from collections import OrderedDict

# TODO gizmos need register maps and bit maps
# that add their names into the assembler setup
# rework address map so it can pre cacluate


class _GizmoCollection:
    " currently unused "

    def __init__(self):
        object.__setattr__(self, "_modules", OrderedDict())

    def __iadd__(self, modules):
        for module in modules:
            self._modules[module] = module
        return self

    def __setattr__(self, name, submodule):
        self._modules[name] = submodule

    def __setitem__(self, name, value):
        return self.__setattr__(name, value)


# TODO create asm definitions named correctly
class BIT:
    " create a named bit register"

    def __init__(self, name, pos):
        self.name = name
        self.pos = pos

    def dump(self, name):
        print("\t" + name + "_" + self.name + " -> " + str(self.pos))


class IO:
    """ 
    Define and bind a read write register
    maps ext_port inside a boneless processor 
    """

    def __init__(self, sig_in=None, sig_out=None, name=None):
        self.sig_in = sig_in
        self.sig_out = sig_out
        self.addr = -1
        self.bits = []
        if name is not None:
            self.name = name

    def set_addr(self, addr):
        self.addr = addr

    def add_bit(self, bit):
        self.bits.append(bit)

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

    def dump(self):
        print(self.name, "-", self.addr)
        for bit in self.bits:
            bit.dump(self.name)

    def __repr__(self):
        return str(self.addr) + "--" + str(self.sig_in) + "--" + str(self.sig_out)


class Gizmo:
    " A gizmo is a wrapper around an Elaboratable module that binds to the external interface of the Boneless-CPU"
    debug = False

    def __init__(self, name, platform=None, **kwargs):
        for i, j in kwargs.items():
            setattr(self, i, j)
        self.platform = platform
        self.name = name
        self.registers = []
        self.devices = []
        self.code = ""  # assembly code for the gizmo TODO , auto attach
        self.build()

    def dump(self):
        for r in self.registers:
            r.dump()

    def build(self):
        " add the modules and IO and BITS to itself"
        print("OVERRIDE ME!")

    def simulator(self):
        " TODO , create interfaces for the simulator"
        print("OVERRIDE ME!")

    def add_device(self, dev):
        " add a Module to the gizmo "
        self.devices.append(dev)

    def add_reg(self, reg):
        " add an Autobinding register to the Boneless CPU"
        self.registers.append(reg)

    def prepare(self, boneless):
        " Build internal and map external bus addresses "
        print("Preparing " + str(self.name) + " within " + str(boneless))
        print(self.registers)
        print(self.devices)
        print("----")
        if len(self.registers) > 0:
            for reg in self.registers:
                reg.set_addr(boneless.addr)
                boneless.addr += 1

    def attach(self, boneless, m, platform):
        " Generate and bind the gateway to the Boneless "
        if self.debug:
            print("<< " + self.name + " >>")
        if len(self.registers) > 0:
            for reg in self.registers:
                with m.If(boneless.ext_port.addr == reg.addr):
                    if reg.has_input():
                        if self.debug:
                            print("Binding Input " + str(reg.addr))
                            print(reg.sig_in)
                        with m.If(boneless.ext_port.r_en):
                            m.d.sync += boneless.ext_port.r_data.eq(reg.sig_in)
                    if reg.has_output():
                        if self.debug:
                            print("Binding Output " + str(reg.addr))
                            print(reg.sig_out)
                        with m.If(boneless.ext_port.w_en):
                            m.d.sync += reg.sig_out.eq(boneless.ext_port.w_data)
                    if self.debug:
                        print()
                        print(self)
        if len(self.devices) > 0:
            for dev in self.devices:
                print(dev)
                m.submodules += dev

    def __repr__(self):
        return (
            "<" + self.name + "|" + str(self.devices) + "|" + str(self.registers) + ">"
        )


class TestGizmo(Gizmo):
    "Test Gizmo"
    code = "NOP"

    def build(self):
        r = IO(Signal(), Signal(), name="first")
        r.add_bit(BIT("bit_a", 0))
        r.add_bit(BIT("bit_b", 1))
        self.add_reg(r)
        r = IO(Signal(), Signal(), name="second")
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
    tg.dump()
    m = Module()
    b = FakeBoneless()
    tg.attach(b, m, None)
