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

  // uart pipeline in
  wire [7:0] uart_in_data;
  wire       uart_in_valid;
  wire       uart_in_ready;
  assign debug = { uart_in_valid, uart_in_ready, reset, clk_48mhz };

  wire usb_p_tx;
  wire usb_n_tx;
  wire usb_p_rx;
  wire usb_n_rx;
  wire usb_tx_en;
  // usb uart - this instanciates the entire USB device.
  usb_uart_i40 uart (
    .clk_48mhz  (clk_48mhz),
    .reset      (reset),

    // pins
    .pin_usb_p( pin_usb_p ),
    .pin_usb_n( pin_usb_n ),

    // uart pipeline in
    .uart_in_data( uart_in_data ),
    .uart_in_valid( uart_in_valid ),
    .uart_in_ready( uart_in_ready ),

    .uart_out_data( uart_in_data ),
    .uart_out_valid( uart_in_valid ),
    .uart_out_ready( uart_in_ready  )

    //.debug( debug )
  );

  assign pin_pu = 1'b1;


// Boneless CPU
// -------------------------

    boneless_core cpu(
        .clk(clk_48mhz),
        .rst(reset),
        .r_win(0),
        .pins(led),
    );
// -------------------------
endmodule
