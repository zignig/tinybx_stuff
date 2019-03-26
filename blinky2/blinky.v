/* Generated by Yosys 0.8+299 (git sha1 ccfa2fe0, clang 6.0.0-1ubuntu2 -fPIC -Os) */

(* generator = "nMigen" *)
module anonymous(LED, clk);
  (* src = "ctr.py:42" *)
  reg \$next\LED ;
  (* src = "ctr.py:42" *)
  output LED;
  (* src = "ctr.py:59" *)
  input clk;
  (* src = "ctr.py:30" *)
  wire o;
  \anonymous$1  \$1  (
    .clk(clk),
    .o(o)
  );
  always @* begin
    \$next\LED  = 1'h0;
    \$next\LED  = o;
  end
  assign LED = \$next\LED ;
endmodule

(* generator = "nMigen" *)
module \anonymous$1 (o, clk);
  wire [21:0] \$1 ;
  wire [21:0] \$2 ;
  (* src = "ctr.py:30" *)
  reg \$next\o ;
  (* src = "ctr.py:29" *)
  reg [20:0] \$next\v ;
  (* src = "ctr.py:59" *)
  input clk;
  (* src = "ctr.py:30" *)
  output o;
  (* init = 21'h1fffff *)
  (* src = "ctr.py:29" *)
  reg [20:0] v = 21'h1fffff;
  assign \$2  = v + (* src = "ctr.py:34" *) 1'h1;
  always @(posedge clk)
      v <= \$next\v ;
  always @* begin
    \$next\v  = v;
    \$next\v  = \$1 [20:0];
  end
  always @* begin
    \$next\o  = 1'h0;
    \$next\o  = v[20];
  end
  assign \$1  = \$2 ;
  assign o = \$next\o ;
endmodule

(* generator = "nMigen" *)
module \anonymous$2 (PIN_12, clk);
  (* src = "ctr.py:42" *)
  reg \$next\PIN_12 ;
  (* src = "ctr.py:42" *)
  output PIN_12;
  (* src = "ctr.py:59" *)
  input clk;
  (* src = "ctr.py:30" *)
  wire o;
  \anonymous$3  \$1  (
    .clk(clk),
    .o(o)
  );
  always @* begin
    \$next\PIN_12  = 1'h0;
    \$next\PIN_12  = o;
  end
  assign PIN_12 = \$next\PIN_12 ;
endmodule

(* generator = "nMigen" *)
module \anonymous$3 (o, clk);
  wire [22:0] \$1 ;
  wire [22:0] \$2 ;
  (* src = "ctr.py:30" *)
  reg \$next\o ;
  (* src = "ctr.py:29" *)
  reg [21:0] \$next\v ;
  (* src = "ctr.py:59" *)
  input clk;
  (* src = "ctr.py:30" *)
  output o;
  (* init = 22'h3fffff *)
  (* src = "ctr.py:29" *)
  reg [21:0] v = 22'h3fffff;
  assign \$2  = v + (* src = "ctr.py:34" *) 1'h1;
  always @(posedge clk)
      v <= \$next\v ;
  always @* begin
    \$next\v  = v;
    \$next\v  = \$1 [21:0];
  end
  always @* begin
    \$next\o  = 1'h0;
    \$next\o  = v[21];
  end
  assign \$1  = \$2 ;
  assign o = \$next\o ;
endmodule

(* generator = "nMigen" *)
module \anonymous$4 (PIN_13, clk);
  (* src = "ctr.py:42" *)
  reg \$next\PIN_13 ;
  (* src = "ctr.py:42" *)
  output PIN_13;
  (* src = "ctr.py:59" *)
  input clk;
  (* src = "ctr.py:30" *)
  wire o;
  \anonymous$5  \$1  (
    .clk(clk),
    .o(o)
  );
  always @* begin
    \$next\PIN_13  = 1'h0;
    \$next\PIN_13  = o;
  end
  assign PIN_13 = \$next\PIN_13 ;
endmodule

(* generator = "nMigen" *)
module \anonymous$5 (o, clk);
  wire [23:0] \$1 ;
  wire [23:0] \$2 ;
  (* src = "ctr.py:30" *)
  reg \$next\o ;
  (* src = "ctr.py:29" *)
  reg [22:0] \$next\v ;
  (* src = "ctr.py:59" *)
  input clk;
  (* src = "ctr.py:30" *)
  output o;
  (* init = 23'h7fffff *)
  (* src = "ctr.py:29" *)
  reg [22:0] v = 23'h7fffff;
  assign \$2  = v + (* src = "ctr.py:34" *) 1'h1;
  always @(posedge clk)
      v <= \$next\v ;
  always @* begin
    \$next\v  = v;
    \$next\v  = \$1 [22:0];
  end
  always @* begin
    \$next\o  = 1'h0;
    \$next\o  = v[22];
  end
  assign \$1  = \$2 ;
  assign o = \$next\o ;
endmodule

(* generator = "nMigen" *)
module \anonymous$6 (PIN_14, clk);
  (* src = "ctr.py:42" *)
  reg \$next\PIN_14 ;
  (* src = "ctr.py:42" *)
  output PIN_14;
  (* src = "ctr.py:59" *)
  input clk;
  (* src = "ctr.py:30" *)
  wire o;
  \anonymous$7  \$1  (
    .clk(clk),
    .o(o)
  );
  always @* begin
    \$next\PIN_14  = 1'h0;
    \$next\PIN_14  = o;
  end
  assign PIN_14 = \$next\PIN_14 ;
endmodule

(* generator = "nMigen" *)
module \anonymous$7 (o, clk);
  wire [24:0] \$1 ;
  wire [24:0] \$2 ;
  (* src = "ctr.py:30" *)
  reg \$next\o ;
  (* src = "ctr.py:29" *)
  reg [23:0] \$next\v ;
  (* src = "ctr.py:59" *)
  input clk;
  (* src = "ctr.py:30" *)
  output o;
  (* init = 24'hffffff *)
  (* src = "ctr.py:29" *)
  reg [23:0] v = 24'hffffff;
  assign \$2  = v + (* src = "ctr.py:34" *) 1'h1;
  always @(posedge clk)
      v <= \$next\v ;
  always @* begin
    \$next\v  = v;
    \$next\v  = \$1 [23:0];
  end
  always @* begin
    \$next\o  = 1'h0;
    \$next\o  = v[23];
  end
  assign \$1  = \$2 ;
  assign o = \$next\o ;
endmodule

(* generator = "nMigen" *)
module \anonymous$8 (PIN_15, clk);
  (* src = "ctr.py:42" *)
  reg \$next\PIN_15 ;
  (* src = "ctr.py:42" *)
  output PIN_15;
  (* src = "ctr.py:59" *)
  input clk;
  (* src = "ctr.py:30" *)
  wire o;
  \anonymous$9  \$1  (
    .clk(clk),
    .o(o)
  );
  always @* begin
    \$next\PIN_15  = 1'h0;
    \$next\PIN_15  = o;
  end
  assign PIN_15 = \$next\PIN_15 ;
endmodule

(* generator = "nMigen" *)
module \anonymous$9 (o, clk);
  wire [25:0] \$1 ;
  wire [25:0] \$2 ;
  (* src = "ctr.py:30" *)
  reg \$next\o ;
  (* src = "ctr.py:29" *)
  reg [24:0] \$next\v ;
  (* src = "ctr.py:59" *)
  input clk;
  (* src = "ctr.py:30" *)
  output o;
  (* init = 25'h1ffffff *)
  (* src = "ctr.py:29" *)
  reg [24:0] v = 25'h1ffffff;
  assign \$2  = v + (* src = "ctr.py:34" *) 1'h1;
  always @(posedge clk)
      v <= \$next\v ;
  always @* begin
    \$next\v  = v;
    \$next\v  = \$1 [24:0];
  end
  always @* begin
    \$next\o  = 1'h0;
    \$next\o  = v[24];
  end
  assign \$1  = \$2 ;
  assign o = \$next\o ;
endmodule

(* top =  1  *)
(* generator = "nMigen" *)
module top(LED, PIN_12, PIN_13, PIN_14, PIN_15, clk);
  (* src = "ctr.py:63" *)
  reg \$next\LED ;
  (* src = "ctr.py:63" *)
  reg \$next\PIN_12 ;
  (* src = "ctr.py:63" *)
  reg \$next\PIN_13 ;
  (* src = "ctr.py:63" *)
  reg \$next\PIN_14 ;
  (* src = "ctr.py:63" *)
  reg \$next\PIN_15 ;
  (* src = "ctr.py:63" *)
  output LED;
  (* src = "ctr.py:42" *)
  wire \LED$1 ;
  (* src = "ctr.py:63" *)
  output PIN_12;
  (* src = "ctr.py:42" *)
  wire \PIN_12$3 ;
  (* src = "ctr.py:63" *)
  output PIN_13;
  (* src = "ctr.py:42" *)
  wire \PIN_13$5 ;
  (* src = "ctr.py:63" *)
  output PIN_14;
  (* src = "ctr.py:42" *)
  wire \PIN_14$7 ;
  (* src = "ctr.py:63" *)
  output PIN_15;
  (* src = "ctr.py:42" *)
  wire \PIN_15$9 ;
  (* src = "ctr.py:59" *)
  input clk;
  \anonymous$8  \$10  (
    .PIN_15(\PIN_15$9 ),
    .clk(clk)
  );
  anonymous \$2  (
    .LED(\LED$1 ),
    .clk(clk)
  );
  \anonymous$2  \$4  (
    .PIN_12(\PIN_12$3 ),
    .clk(clk)
  );
  \anonymous$4  \$6  (
    .PIN_13(\PIN_13$5 ),
    .clk(clk)
  );
  \anonymous$6  \$8  (
    .PIN_14(\PIN_14$7 ),
    .clk(clk)
  );
  always @* begin
    \$next\LED  = 1'h0;
    \$next\LED  = \LED$1 ;
  end
  always @* begin
    \$next\PIN_12  = 1'h0;
    \$next\PIN_12  = \PIN_12$3 ;
  end
  always @* begin
    \$next\PIN_13  = 1'h0;
    \$next\PIN_13  = \PIN_13$5 ;
  end
  always @* begin
    \$next\PIN_14  = 1'h0;
    \$next\PIN_14  = \PIN_14$7 ;
  end
  always @* begin
    \$next\PIN_15  = 1'h0;
    \$next\PIN_15  = \PIN_15$9 ;
  end
  assign PIN_15 = \$next\PIN_15 ;
  assign PIN_14 = \$next\PIN_14 ;
  assign PIN_13 = \$next\PIN_13 ;
  assign PIN_12 = \$next\PIN_12 ;
  assign LED = \$next\LED ;
endmodule