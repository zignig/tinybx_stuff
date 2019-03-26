module top(...);
    input CLK;
    output LED;
    blinky b(
        .clk(CLK),
        .rst(0),
        .o(LED),
    );
endmodule
