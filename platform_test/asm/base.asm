NOP
NOP

wait:
    SUBI R2, 1
    CMP R2,R3
    JNZ wait
JR R7,0

loop:
    STX R1, R0, 0
    ADDI R1, 1
    MOVL R2,255
    MOVH R2,255
    JAL R7,wait
    J loop
