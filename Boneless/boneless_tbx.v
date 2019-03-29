module boneless_tbx(
    inout  pin_usb_p,
    inout  pin_usb_n,
    output pin_pu,
    input clk,
    output [3:0] led
);
    wire clk_48mhz;
    wire clk_locked;
    // Use an icepll generated pll
    pll pll48( .clock_in(clk), .clock_out(clk_48mhz), .locked( clk_locked ) );

    // Generate reset signal
    reg [5:0] reset_cnt = 0;
    wire reset = ~reset_cnt[5];
    always @(posedge clk_48mhz)
        if ( clk_locked )
            reset_cnt <= reset_cnt + reset;
    // -------------------------
    // USB serial
    // interface to the boneless cpu
    wire [2:0] usb_in_control;
    wire [7:0] usb_in_data;
    wire [2:0] usb_out_control;
    wire [7:0] usb_out_data;
    //assign debug = { uart_in_valid, uart_in_ready, reset, clk_48mhz };

    // usb uart - this instanciates the entire USB device.
    usb_uart_i40 uart (
        .clk_48mhz  (clk_48mhz),
        .reset      (reset),

        // pins
        .pin_usb_p( pin_usb_p ),
        .pin_usb_n( pin_usb_n ),

        // uart pipeline in
        .uart_in_data( usb_in_data),
        .uart_in_valid( usb_in_control[0]),
        .uart_in_ready( usb_in_control[1]),

        .uart_out_data( usb_out_data),
        .uart_out_valid( usb_out_control[0]),
        .uart_out_ready( usb_out_control[1])

        //.debug( debug )
    );


    assign pin_pu = 1'b1;

    // Boneless CPU
    // -------------------------
    boneless_core cpu(
        .clk(clk_48mhz),
        .rst(reset),
        .r_win(0),
        .usb_in_control(usb_in_control),
        .usb_out_control(usb_out_control),
        .usb_in_data(usb_in_data),
        .usb_out_data(usb_out_data),
        .pins(led),
    );
    // -------------------------
endmodule
