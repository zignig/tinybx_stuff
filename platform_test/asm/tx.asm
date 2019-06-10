J init

.macro delay 
    MOVL R5,255
    MOVH R5,55
    JAL R7,wait
.endm

.macro multi
    delay
    delay
    delay
    delay
.endm 

init:
    MOVL R4,48 
    MOVH R4,0
    MOVL R1,90
    MOVH R1,0
loop:
    STX R4, R0, 2 
    MOVL R3,1     
    STX R3, R0, 1 
    MOVL R3,0     
    STX R3, R0, 1 
    ADDI R4,1
    multi
    J loop

wait:
    SUBI R5, 1
    CMP R5,R6
    JNZ wait
    JR R7,0
