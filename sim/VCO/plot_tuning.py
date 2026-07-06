#!/usr/bin/env python3
"""Plot the LELO_VCO tuning curve (fout vs Vin) from vco_tuning.dat.

vco_tuning.dat is produced by `make sweep` (ngspice sweep.spi) and has two
whitespace-separated columns:  Vin[V]   fout[Hz].
Non-oscillating / invalid points (fout <= 0) are dropped automatically.
"""
import os
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

HERE = os.path.dirname(os.path.abspath(__file__))
DAT = os.path.join(HERE, "vco_tuning.dat")
PNG = os.path.join(HERE, "vco_tuning_curve.png")

vin, fout = [], []
with open(DAT) as f:
    for line in f:
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        parts = line.split()
        if len(parts) < 2:
            continue
        try:
            v, fo = float(parts[0]), float(parts[1])
        except ValueError:
            continue
        if fo <= 0 or fo > 1e9:          # drop non-oscillating points
            continue
        vin.append(v)
        fout.append(fo / 1e6)            # Hz -> MHz

vin = np.array(vin)
fout = np.array(fout)

# VCO gain (K_VCO) from the near-linear region
lin = (vin >= 0.5) & (vin <= 1.3)
kvco = np.polyfit(vin[lin], fout[lin], 1)[0]     # MHz/V

plt.style.use("seaborn-v0_8-whitegrid")
fig, ax = plt.subplots(figsize=(7.5, 5))
ax.plot(vin, fout, "o-", color="#2563eb", lw=2, ms=7, mfc="white",
        mec="#2563eb", mew=1.8, label="f_out (sim)")
ax.axvspan(0.5, 1.3, color="#2563eb", alpha=0.06,
           label=f"linear region (K$_{{VCO}}$ ≈ {kvco:.0f} MHz/V)")

ax.set_xlabel("Control voltage  V$_{in}$  [V]", fontsize=12)
ax.set_ylabel("Output frequency  f$_{out}$  [MHz]", fontsize=12)
ax.set_title("LELO_VCO Tuning Curve\n(typical corner, 27 °C, VDD = 1.8 V)",
             fontsize=13, fontweight="bold")
ax.set_xlim(0.4, 1.85)
ax.set_ylim(0, fout.max() * 1.12)
ax.legend(frameon=True, fontsize=10, loc="lower right")

for v, fo in zip(vin, fout):
    if v in (0.9, 1.8):
        ax.annotate(f"{fo:.1f} MHz\n@ {v:.1f} V", xy=(v, fo),
                    xytext=(0, 12), textcoords="offset points",
                    ha="center", fontsize=9, color="#111")

fig.tight_layout()
fig.savefig(PNG, dpi=150)
print(f"Saved {PNG}")
print(f"K_VCO (0.5-1.3 V) = {kvco:.1f} MHz/V")
print(f"Range: {fout.min():.1f} .. {fout.max():.1f} MHz "
      f"over Vin {vin.min():.2f} .. {vin.max():.2f} V")
