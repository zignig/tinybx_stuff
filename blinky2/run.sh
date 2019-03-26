#!/bin/sh -ex

cd $(dirname $0)
python3 ctr.py generate blinky.v
#python3 -m boneless.gateware.core_fsm  pins generate fsm_core_pins.v
yosys blinky.v -p "synth_ice40 -top top -json blinky.json"
nextpnr-ice40 --placer heap --hx8k --package cm81 --pcf pins.pcf --json blinky.json --asc blinky.txt
icepack blinky.txt blinky.bin
tinyprog -p blinky.bin

