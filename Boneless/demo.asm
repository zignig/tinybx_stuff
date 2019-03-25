J init
.macro on 
    MOVI R3,1
    STX R3,R7,0
.endm

.macro off
    MOVI R3,0
    STX R3,R7,0
.endm

MOVI R1, 8192 

init:
    ADDI R1,10
    MOVI R2,0
    on
loop1:
    ADDI R2,1
    CMP R2,R1
    JE eloop1
    J loop1
eloop1:
    off
    MOVI R2,0
loop2:
    ADDI R2,1
    CMP R2,R1
    JE init
    J loop2
