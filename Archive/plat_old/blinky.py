from nmigen import *
from nmigen_boards.tinyfpga_bx import *
from plat import BB
from _blinky import build_and_program 

if __name__ == "__main__":
    platform = BB()
    build_and_program(BB,'clk16') 
