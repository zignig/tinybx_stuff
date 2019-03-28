J init
.macro on 
    ADDI R0,1
    STX R0,R4,0
.endm

.macro off
    MOVI R3,0
    STX R3,R4,0
.endm


wait:
    MOVI R2,0
waiter:
    ADDI R2,1
    CMP R2,R1
    JE ex
    J waiter 
ex:
    JR R7,0

.macro WAIT
    JAL R7, wait
.endm

.macro long
    WAIT
    WAIT
    WAIT
    WAIT
.endm

init:
    MOVI R1,10000
blink:
    on
    long 
    off
    long
J blink 

