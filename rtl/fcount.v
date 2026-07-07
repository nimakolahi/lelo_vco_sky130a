//----------------------------------------------------------------------
// fcount - VCO frequency counter
//
// Counts rising edges of `clk` (the VCO output) during a measurement
// window defined by `gate`.  While `gate` is high the counter increments
// on every VCO edge; when `gate` falls the final tally is latched into
// `result`.  With a known gate width T_gate the measurement is
//
//     result = f_out * T_gate      (number of VCO cycles in the window)
//
// so `result` is a digital code proportional to f_out, and hence to the
// VCO control voltage Vin - the read-out for the VCO-based voltage sensor.
//----------------------------------------------------------------------
module fcount #(parameter W = 11) (
    input  wire          clk,     // measured clock (VCO output)
    input  wire          gate,    // measurement window: count while high
    output logic [W-1:0] count,   // live running count
    output logic [W-1:0] result   // latched count captured at window end
    );

   logic gate_q;

   always_ff @(posedge clk) begin
      gate_q <= gate;
      if (!gate) begin
         if (gate_q)             // falling edge of gate -> capture result
           result <= count;
         count <= '0;
      end else begin
         count <= count + 1'b1;
      end
   end

endmodule
