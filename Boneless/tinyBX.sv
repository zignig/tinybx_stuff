module top(...);

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
    input clk;
    output [3:0] led;

    boneless cpu(
        .clk(clk_48mhz),
        .rst(reset),
        .r_win(0),
        .pins(led),
    );
endmodule
