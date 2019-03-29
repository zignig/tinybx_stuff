MOV R7,1
here:
    NOP
    LDX R0,R7,0
    STX R0,R2,0
J here
;.def c_in, R4
;.def d_in, R5
;.def c_out, R6
;.def d_out, R7
;
;
;wait:
;    MOVI R2,0
;waiter:
;    ADDI R2,1
;    CMP R2,R1
;    JE ex
;    J waiter 
;ex:
;    JR R7,0
;
;.macro WAIT
;    JAL R7, wait
;.endm
;
;.macro long
;    WAIT
;    WAIT
;    WAIT
;    WAIT
;.endm
;
;MOVL c_in,10
;MOVL d_in,11
;MOVL c_out,12
;MOVL d_out,13
;MOVI R2,50000
;MOVL R1,0
;MOVL R3,0
;init:
;    LDX R0,c_in,0
;    STX R0,R3,0
;;    STX R3,c_out,0
;;    STX R0,d_out,0
;;    CMP R0,R3
;;    JE out
;;    long
;;    long
;;    long
;;    J init
;;out:
;;    MOVL R0,32
;J init
