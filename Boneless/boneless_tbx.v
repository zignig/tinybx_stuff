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
    wire [7:0] usb_in_data;
    wire usb_in_valid;
    wire usb_in_ready;
    
    wire [7:0] usb_out_data;
    wire usb_out_valid;
    wire usb_out_ready;
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
        .uart_in_valid( usb_in_valid),
        .uart_in_ready( usb_in_ready),

        .uart_out_data( usb_out_data),
        .uart_out_valid( usb_out_valid),
        .uart_out_ready( usb_out_valid)

        //.debug( debug )
    );

    // the pull up
    assign pin_pu = 1'b1;

//  // uart pipeline in (out of the device, into the host)
//  input [7:0] uart_in_data,
//  input       uart_in_valid,
//  output      uart_in_ready,

//  // uart pipeline out (into the device, out of the host)
//  output [7:0] uart_out_data,
//  output       uart_out_valid,
//  input        uart_out_ready,

// This is the shape and direction of the uart

// 16 bit word for the boneless
    wire [15:0] usbout;
    wire [15:0] usbin;
// concat
    assign usbin = {usb_in_data,usb_out_ready,usb_in_valid};
    assign usbout = {usb_out_data,usb_in_ready,usb_out_valid};

    // Boneless CPU
    // -------------------------
    boneless_core cpu(
        .clk(clk_48mhz),
        .rst(reset),
        .r_win(0),
        //.usbout(usbout),
        .usbin(usbin),
        .pins(led),
    );
    // -------------------------
endmodule
