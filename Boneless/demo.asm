J init
.macro on 
    MOVI R3,1
    STX R3,R7,0
.endm

.macro off
    MOVI R3,0
    STX R3,R7,0
.endm

MOVI R1, 0

init:
    ADDI R1,1
    on
loop1:
    ADDI R2,1
    CMP R2,R1
    JE eloop1
    J loop1
eloop1:
    off
loop2:
    SUBI R2,1
    CMP R2,R4
    JE init
    J loop2
