#!/bin/sh -ex

cd $(dirname $0)
python3 processor.py generate build/fsm_core_pins.v
yosys build/fsm_core_pins.v pll.v tinyBX.sv -p "synth_ice40 -top top -json build/tinyBX.json"
nextpnr-ice40 --placer heap --hx8k --package cm81 --pcf tinyBX.pcf --json build/tinyBX.json --asc build/tinyBX.txt
icepack build/tinyBX.txt build/tinyBX.bin
tinyprog -p build/tinyBX.bin
