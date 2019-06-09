module top(...);
    input CLK;
    output PIN_15;
    blinky b(
        .clk(CLK),
        .rst(0),
        .o(PIN_15),
    );
endmodule
