module top(...);
    input CLK;
    output PIN_12;
    blinky b(
        .clk(CLK),
        .rst(0),
        .o(PIN_12),
    );
endmodule
