#!/usr/bin/env python3
"""LELO_VCO tuning-curve spread across PVT corners.

For each corner (process / temperature / supply) this runs an ngspice Vin
sweep, measures f_out at each point, and overlays the tuning curves to show
the min/typ/max envelope.

Run with:  make sweep_corners   (inside the wulffern/aicex container)
Outputs:   vco_tuning_corners.dat, vco_tuning_corners.png
"""
import os
import re
import subprocess
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

HERE = os.path.dirname(os.path.abspath(__file__))
NETLIST = "../../work/xsch/LELO_VCO.spice"
LIB = "$PDK_ROOT/sky130A/libs.tech/ngspice/sky130.lib.spice"

# label, process corner, temp [C], VDD [V], colour
CORNERS = [
    ("Fast  (ff, -40 C, 1.98 V)", "ff", -40, 1.98, "#dc2626"),
    ("Typ   (tt,  27 C, 1.80 V)", "tt", 27, 1.80, "#2563eb"),
    ("Slow  (ss, 125 C, 1.62 V)", "ss", 125, 1.62, "#059669"),
]

VIN_STEPS = ["0.30", "0.40", "0.50", "0.60", "0.70", "0.80", "0.90",
             "1.00", "1.10", "1.20", "1.30", "1.40", "1.50", "1.60",
             "1.70", "1.80"]

DECK = """* LELO_VCO corner tuning sweep
.include {netlist}
.lib "{lib}" {corner}
.temp {temp}
.option TNOM=27 GMIN=1e-15 reltol=1e-3
.param AVDD={vdd}

VSS VSS 0        dc 0
VDD VDD_1V8 VSS  pwl 0 0 10n {{AVDD}}
VIN Vin VSS      dc 0.9

XDUT VDD_1V8 VSS Vin Vout LELO_VCO

.control
  set num_threads=8
  unset askquit
  foreach vv {steps}
    alter @VIN[dc] = $vv
    tran 20p 3u
    let t1 = 0
    let t2 = 0
    meas tran t1 WHEN v(Vout)={mid} RISE=3
    meas tran t2 WHEN v(Vout)={mid} RISE=8
    let fosc = 5/(t2-t1)
    echo "RESULT $vv" $&fosc
  end
  quit
.endc
.end
"""


def run_corner(corner, temp, vdd):
    deck = DECK.format(netlist=NETLIST, lib=LIB, corner=corner, temp=temp,
                       vdd=vdd, steps=" ".join(VIN_STEPS), mid=vdd / 2.0)
    deck_path = os.path.join(HERE, f"_corner_{corner}.spi")
    with open(deck_path, "w") as f:
        f.write(deck)
    out = subprocess.run(["ngspice", "-b", deck_path], cwd=HERE,
                         capture_output=True, text=True).stdout
    os.remove(deck_path)
    vin, fout = [], []
    for line in out.splitlines():
        m = re.match(r"RESULT\s+([\d.]+)\s+([-\d.Ee+]+)\s*$", line.strip())
        if not m:
            continue
        v, fo = float(m.group(1)), float(m.group(2))
        if fo <= 0 or fo > 1e9:
            continue
        vin.append(v)
        fout.append(fo / 1e6)
    return np.array(vin), np.array(fout)


results = {}
for label, corner, temp, vdd, color in CORNERS:
    print(f"Running {label} ...", flush=True)
    results[label] = (run_corner(corner, temp, vdd), color)

# write combined data
with open(os.path.join(HERE, "vco_tuning_corners.dat"), "w") as f:
    f.write("# corner   Vin[V]   fout[MHz]\n")
    for label, ((vin, fout), _) in results.items():
        tag = label.split("(")[1].split(",")[0].strip()
        for v, fo in zip(vin, fout):
            f.write(f"{tag:4s}  {v:.3f}  {fo:.4f}\n")

# plot
plt.style.use("seaborn-v0_8-whitegrid")
fig, ax = plt.subplots(figsize=(7.5, 5))

fast = results[CORNERS[0][0]][0]
slow = results[CORNERS[2][0]][0]
common = sorted(set(fast[0]).intersection(set(slow[0])))
if common:
    fd = dict(zip(fast[0], fast[1]))
    sd = dict(zip(slow[0], slow[1]))
    cx = np.array(common)
    ax.fill_between(cx, [sd[v] for v in common], [fd[v] for v in common],
                    color="#94a3b8", alpha=0.20, label="PVT spread")

for label, ((vin, fout), color) in results.items():
    ax.plot(vin, fout, "o-", color=color, lw=2, ms=6, mfc="white",
            mec=color, mew=1.6, label=label)

ax.set_xlabel("Control voltage  V$_{in}$  [V]", fontsize=12)
ax.set_ylabel("Output frequency  f$_{out}$  [MHz]", fontsize=12)
ax.set_title("LELO_VCO Tuning Curve across PVT corners", fontsize=13,
             fontweight="bold")
ax.set_xlim(0.35, 1.85)
ax.set_ylim(0, None)
ax.legend(frameon=True, fontsize=9, loc="upper left")
fig.tight_layout()
png = os.path.join(HERE, "vco_tuning_corners.png")
fig.savefig(png, dpi=150)
print("Saved", png)
for label, ((vin, fout), _) in results.items():
    if len(fout):
        print(f"  {label}: {fout.min():.1f} .. {fout.max():.1f} MHz")
