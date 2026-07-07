#!/usr/bin/env python3
"""Digital transfer curve of the VCO + counter: measured count vs Vin.

For each control voltage Vin, co-simulates the analog VCO with the RTL counter
(d_cosim) over a fixed gate window and records the latched count. The result is
the ADC-style transfer characteristic (digital code vs input voltage).

Requires the compiled model + instance (run `make rtl` first, which the Makefile
`sweep` target does). Outputs fcount_transfer.dat and fcount_transfer.png.
"""
import os
import re
import subprocess
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

HERE = os.path.dirname(os.path.abspath(__file__))
TGATE = 2e-6
VIN_STEPS = [round(0.3 + 0.1 * i, 2) for i in range(16)]  # 0.30 .. 1.80

DECK = """*VCO + fcount transfer sweep
.include ../../work/xsch/LELO_VCO.spice
.lib "$PDK_ROOT/sky130A/libs.tech/ngspice/sky130.lib.spice" tt
.temp 27
.option TNOM=27 GMIN=1e-15 reltol=1e-3 method=gear
.param AVDD=1.8
.param VIN={vin}
.param TSTART=0.5u
.param TGATE=2u

VSS  VSS 0        dc 0
VDD  VDD_1V8 VSS  pwl 0 0 10n {{AVDD}}
VINP Vin VSS      dc {{VIN}}
VGATE gate 0 pwl 0 0 {{TSTART}} 0 {{TSTART+1n}} {{AVDD}} {{TSTART+TGATE}} {{AVDD}} {{TSTART+TGATE+1n}} 0

XDUT VDD_1V8 VSS Vin Vout LELO_VCO
VLINK clk Vout dc 0
.include svinst.spi

.control
  set num_threads=8
  unset askquit
  pre_set auto_bridge_d_out =
     + ( ".model auto_dac dac_bridge(out_low = 0.0 out_high = 1.8)"
     +   "auto_bridge%d [ %s ] [ %s ] auto_dac" )
  optran 0 0 0 1n 1u 0
  tran 20p 3u
  let idx = length(v(dec_result)) - 1
  let ncount = v(dec_result)[idx]*1000
  echo "RESULT {vin}" $&ncount
  quit
.endc
.end
"""


def run(vin):
    deck = DECK.format(vin=vin)
    path = os.path.join(HERE, f"_sweep_{vin}.spi")
    with open(path, "w") as f:
        f.write(deck)
    out = subprocess.run(["ngspice", "-b", path], cwd=HERE,
                         capture_output=True, text=True).stdout
    os.remove(path)
    for line in out.splitlines():
        m = re.match(rf"RESULT\s+{vin}\s+([-\d.Ee+]+)", line.strip())
        if m:
            return round(float(m.group(1)))
    return None


vin, code = [], []
for v in VIN_STEPS:
    n = run(v)
    print(f"  Vin={v:.2f} -> count={n}", flush=True)
    if n is not None and n > 0:
        vin.append(v)
        code.append(n)

vin = np.array(vin)
code = np.array(code)

with open(os.path.join(HERE, "fcount_transfer.dat"), "w") as f:
    f.write(f"# gate window = {TGATE*1e6:.0f} us\n# Vin[V]  count\n")
    for v, c in zip(vin, code):
        f.write(f"{v:.3f}  {c}\n")

# LSB (counts/volt) from the linear region
lin = (vin >= 0.5) & (vin <= 1.3)
slope = np.polyfit(vin[lin], code[lin], 1)[0]  # counts / V

plt.style.use("seaborn-v0_8-whitegrid")
fig, ax = plt.subplots(figsize=(7.5, 5))
ax.step(vin, code, where="mid", color="#7c3aed", lw=1.2, alpha=0.5)
ax.plot(vin, code, "o", color="#7c3aed", ms=7, mfc="white", mec="#7c3aed",
        mew=1.8, label="counter code (sim)")
ax.axvspan(0.5, 1.3, color="#7c3aed", alpha=0.06,
           label=f"linear region ({slope:.0f} counts/V)")
ax.set_xlabel("Control voltage  V$_{in}$  [V]", fontsize=12)
ax.set_ylabel(f"Counter code  (over {TGATE*1e6:.0f} µs gate)", fontsize=12)
ax.set_title("LELO_VCO + fcount: digital transfer characteristic\n"
             "(typical, 27 °C, VDD = 1.8 V)", fontsize=13, fontweight="bold")
ax.set_xlim(0.4, 1.85)
ax.set_ylim(0, code.max() * 1.12)
ax.legend(loc="upper left", fontsize=10, frameon=True)
fig.tight_layout()
png = os.path.join(HERE, "fcount_transfer.png")
fig.savefig(png, dpi=150)
print("Saved", png)
print(f"sensitivity ~= {slope:.1f} counts/V  ({slope/(TGATE*1e6):.1f} counts/V per us... "
      f"= {slope:.0f} LSB/V over {TGATE*1e6:.0f}us)")
