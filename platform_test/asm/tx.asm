J init
; Some delay macros 

wait:
    SUBI R5, 1
    CMP R5,R6
    JNZ wait
    JR R7,0

.macro delay 
    MOVL R5,255
    MOVH R5,255
    JAL R7,wait
.endm

.macro multi
    delay
    delay
    delay
    delay
.endm 
.string bob, "this is test"

; 
init:
    MOVL R4,0 
    MOVH R4,48
    MOVL R1,90
    MOVH R1,0
loop:
    MOVL R0,1
    STX R4, R0, 0 
    MOVH R0,1
    STX R3, R0, 0 
    MOVL R3,0     
    STX R3, R0, 0 
    CMP R1,R4
    JE init
    ADDI R4,1
    delay
    J loop

