#!/bin/sh -ex

cd $(dirname $0)
python3 processor.py generate fsm_core_pins.v
#python3 -m boneless.gateware.core_fsm  pins generate fsm_core_pins.v
yosys fsm_core_pins.v tinyBX.sv -p "synth_ice40 -top top -json tinyBX.json"
nextpnr-ice40 --placer heap --hx8k --package cm81 --pcf tinyBX.pcf --json tinyBX.json --asc tinyBX.txt
icepack tinyBX.txt tinyBX.bin
tinyprog -p tinyBX.bin

