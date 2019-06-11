Run python construct.py to build and program a tinyfpga_bx

Edit the platform in plat.py to alter your hardware setup.

Edit construct.py to add new gizmos , these will auto bind to the boneless memory map.

# TODO
- add bound names to the assembler 
- expose and emulate gizmos in the simulator 
- get UART working 
- test echo program
- get flash read write working 
- get monitor working 
- rework simulator for new style boneless
- cleanse Boneless-CPU branch and get it merged upstream
- write and document some more cores
