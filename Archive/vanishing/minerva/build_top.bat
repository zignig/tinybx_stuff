@rem Automatically generated by nMigen d5ba26b. Do not edit.
@echo off
yosys -q -l top.rpt top.ys || exit /b
nextpnr-ice40 --quiet --placer heap --log top.tim --lp8k --package cm81 --json top.json --pcf top.pcf --pre-pack top_pre_pack.py --asc top.asc || exit /b
icepack top.asc top.bin || exit /b