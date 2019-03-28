##
## Make and program TinyFPGA BX
## Boneless from
##

BASENAME = boneless
TARGETNAME = $(BASENAME)_tbx
PROJTOP = $(TARGETNAME)

SOURCES = boneless_core.v usb/*.v pll.v

SRC = $(PROJTOP).v $(SOURCES)

PIN_DEF = tinyBX.pcf

DEVICE = lp8k
PACKAGE = cm81

CLK_MHZ = 48

all: $(PROJTOP).rpt $(PROJTOP).bin

pll.v:
	icepll -i 16 -o $(CLK_MHZ) -m -f $@

synth: $(PROJTOP).json

$(PROJTOP).json: $(SRC)
	yosys -q -p 'synth_ice40 -top $(PROJTOP) -json $@' $^

%.asc: $(PIN_DEF) %.json
	nextpnr-ice40 --placer heap --$(DEVICE) --package $(PACKAGE) --pcf $(PIN_DEF) --json $*.json --asc $@

gui: $(PIN_DEF) $(PROJTOP).json
	nextpnr-ice40 --$(DEVICE) --package $(PACKAGE) --pcf $(PIN_DEF) --json $(PROJTOP).json --asc $(PROJTOP).asc --gui

%.v:
	python3 processor.py generate boneless_core.v
%.bin: %.asc
	icepack $< $@

%.rpt: %.asc
	icetime -d $(DEVICE) -mtr $@ $<

prog: $(PROJTOP).bin
	tinyprog -p $<

clean:
	rm -f $(PROJTOP).json $(PROJTOP).asc $(PROJTOP).rpt $(PROJTOP).bin pll.v

.SECONDARY:
.PHONY: all synth prog clean gui
