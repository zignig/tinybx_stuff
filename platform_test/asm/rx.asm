; Read from the uart
; Initial testing 20130612
; Simon Kirkby
; obeygiantrobot@gmail.com

.equ rx_status,2
.equ rx_data,3
.equ tx_status,4
.equ tx_data,5
.equ loop_size,5

J init ; Jump to init 

.def data,R0    ; redfine the name of register 1 to data 
.def addr,R1    ; and again , R1 to addr
.def status,R2
.def led_counter,R3 
.def zero,R4    ; leave as zero for compares
.def leds,R5    ; 
.def ledtop,R6
.def ret,R7     ; subroutine return

.macro call, address
    JAL ret,$address
.endm

.macro return
    JR ret,0
.endm

idle:
    STX leds,addr,1
    ADDI led_counter,1
    CMP led_counter,ledtop
    JE inc_led
    return

inc_led:
    STX leds,zero,0     ; put the led register onto the leds 
    MOVI led_counter,0 ; reset the led counter
    ADDI leds,1         ; increment the led counter
    return

init:           ; label this part in the code
    MOVI addr,rx_status
    MOVI led_counter,1
    MOVI ledtop,loop_size
loop:
    NOP ; do nothing for 1 cycle
    LDX data,addr,0 ; load external memory at addr into data
    CMP data,status ; is the status 0
    JE do_idle 
    J loop

do_idle:
    NOP
    NOP
    NOP
    call idle 
    J loop ; 

incoming: ; there is a character in the io buffer
    ;LDX data,zero,3 ; load the read data
    ;MOVL data,1
    ;ADDI leds,1     ; incr the leds on char
    STX leds,zero,0 ; store the leds 
    ;STX data,addr,0 ; ack the char
    J loop    
