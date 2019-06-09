J init

.macro delay 
    MOVL R2,255
    MOVH R2,255
    JAL R7,wait
.endm

.macro multi
    delay
    delay
    delay
    delay
.endm 

init:
    NOP
    MOVL R4,48 
    MOVL R5,0
loop:
    STX R1, R0,0
    ADDI R1, 1
    MOVL R3,1
    STX R3, R0, 1
    MOVL R3,0
    STX R3, R0, 1
    STX R4, R0, 2
    ADDI R4,1
    J loop

wait:
    SUBI R2, 1
    CMP R2,R3
    JNZ wait
    JR R7,0
