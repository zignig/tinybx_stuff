// look in pins.pcf for all the pin names on the TinyFPGA BX board
module top (
    input CLK,    // 16MHz clock
    output PIN_12,   // User/boot LED next to power LED
    output PIN_13,   // User/boot LED next to power LED
    output PIN_14,   // User/boot LED next to power LED
    output PIN_15,   // User/boot LED next to power LED
    output USBPU  // USB pull-up resistor
);
    // drive USB pull-up resistor to '0' to disable USB
    assign USBPU = 0;

    ////////
    // make a simple blink circuit
    ////////

    // keep track of time and location in blink_pattern
    reg [25:0] blink_counter;

    // pattern that will be flashed over the LED over time
    wire [31:0] blink_pattern0 = 32'b101010001110111011100010101;
    wire [31:0] blink_pattern1 = 32'b101010101010111011100010101;
    wire [31:0] blink_pattern2 = 32'b101010001110111001100110101;
    wire [31:0] blink_pattern3 = 32'b101010001110111010101010101;

    // increment the blink_counter every clock
    always @(posedge CLK) begin
        blink_counter <= blink_counter + 1;
    end
    
    // light up the LED according to the pattern
    assign PIN_12 = blink_pattern0[blink_counter[25:21]];
    assign PIN_13 = blink_pattern1[blink_counter[25:21]];
    assign PIN_14 = blink_pattern2[blink_counter[25:21]];
    assign PIN_15 = blink_pattern3[blink_counter[25:21]];
endmodule
