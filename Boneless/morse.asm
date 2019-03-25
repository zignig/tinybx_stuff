; Morse code flasher
; Simon Kirkby
; obeygiantrobot@gmail.com
; 20190325
;

; name the register for work.

.def DATA, R0
.def ADDR, R1
.def COUNTER, R2
.def MAX , R3
.def OUT, R4
.def LETTER , R5

.def RTN, R7

; helper macros
.macro _call,val
    JAL RTN, $val
.endm

.macro _return
    JR RTN,0
.endm

.macro BRK
    STX OUT,OUT,1
.endm

.macro out
    STX DATA,OUT,0
.endm

; Jump to init 
J init
NOP

; The message to display
.string message,"think global act local"

alpha_address:
    .@ alpha

init:
    MOVA ADDR, message
    LD MAX, ADDR ,0
    ADD MAX,ADDR,MAX
char_loop:
    LD DATA, ADDR ,0
    out
    _call morse_char
    CMP ADDR,MAX
    JE char_loop_out
    ADDI ADDR,1
    J char_loop
char_loop_out:
    BRK
J init

morse_char: ; output each char
    SUBI DATA,97 ; off set for 'a', move back to zero
    MOVA LETTER,alpha
    ADD LETTER,DATA,LETTER
;    LD DATA,LETTER,0
_return

; letter and numbers map
alpha:
    .@ a
    .@ b
    .@ c
    .@ d
    .@ e
    .@ f
    .@ g
    .@ h
    .@ i
    .@ j
    .@ k
    .@ l
    .@ m
    .@ n
    .@ o
    .@ p
    .@ q
    .@ r
    .@ s
    .@ t
    .@ u
    .@ v
    .@ w
    .@ x
    .@ y
    .@ z
number:
    .@ D0
    .@ D1
    .@ D2
    .@ D3
    .@ D4
    .@ D6
    .@ D7
    .@ D8
    .@ D9
NOP
NOP
; Morse code letters
.string a,".-"
.string b,"-..."
.string c,"-.-."
.string d,"-.."
.string e,"."
.string f,"..-."
.string g,"--."
.string h,"...."
.string i,".."
.string j,".---"
.string k,"-.-"
.string l,".-.."
.string m,"--"
.string n,"-."
.string o,"---"
.string p,".--."
.string q,"--.-"
.string r,".-."
.string s,"..."
.string t,"-"
.string u,"..-"
.string v,"...-"
.string w,".--"
.string x,"-..-"
.string y,"-.--"
.string z,"--.."
.string D0,"-----"
.string D1,".----"
.string D2,"..---"
.string D3,"...--"
.string D4,"....-"
.string D5,"....."
.string D6,"-...."
.string D7,"--..."
.string D8,"---.."
.string D9,"----."



