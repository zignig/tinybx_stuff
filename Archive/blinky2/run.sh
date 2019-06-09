#!/bin/sh -ex

cd $(dirname $0)
python3 blinky.py generate build/blinky.v
yosys build/blinky.v -p "synth_ice40 -top top -json build/blinky.json"
nextpnr-ice40 --placer heap --hx8k --package cm81 --pcf pins.pcf --json build/blinky.json --asc build/blinky.txt
icepack build/blinky.txt build/blinky.bin
tinyprog -p build/blinky.bin

