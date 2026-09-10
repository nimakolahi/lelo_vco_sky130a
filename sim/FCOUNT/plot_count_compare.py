#!/usr/bin/env python3
"""Schematic vs post-layout digital transfer curve for LELO_VCO + fcount.

Reads fcount_transfer.dat (schematic) and fcount_transfer_lay.dat
(post-layout, analog half from the extracted netlist) and overlays them.
The counter code IS the sensor output, so the gap between the curves is a
direct gain error if a design is calibrated on schematic numbers.
"""
import os
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

HERE = os.path.dirname(os.path.abspath(__file__))
TGATE_US = 16

def load(fn):
    v, c = [], []
    with open(os.path.join(HERE, fn)) as f:
        for line in f:
            if line.startswith("#"):
                continue
            p = line.split()
            if len(p) < 2:
                continue
            v.append(float(p[0])); c.append(float(p[1]))
    return np.array(v), np.array(c)

def sens(v, c, lo=0.5, hi=1.3):
    m = (v >= lo) & (v <= hi)
    return np.polyfit(v[m], c[m], 1)[0]

vs, cs = load("fcount_transfer.dat")
vl, cl = load("fcount_transfer_lay.dat")
ks, kl = sens(vs, cs), sens(vl, cl)

plt.style.use("seaborn-v0_8-whitegrid")
fig, ax = plt.subplots(figsize=(7.5, 5))
ax.plot(vs, cs, "o-", color="#2563eb", ms=6, mfc="white", mew=1.6,
        label=f"schematic   ({ks:.0f} counts/V)")
ax.plot(vl, cl, "s--", color="#dc2626", ms=6, mfc="white", mew=1.6,
        label=f"post-layout ({kl:.0f} counts/V)")
ax.axvspan(0.5, 1.3, color="#7c3aed", alpha=0.06, label="linear region")
ax.set_xlabel("Control voltage  V$_{in}$  [V]", fontsize=12)
ax.set_ylabel(f"Counter code  (over {TGATE_US} µs gate)", fontsize=12)
ax.set_title("LELO_VCO + fcount: digital transfer, schematic vs post-layout\n"
             "(typical, 27 °C, VDD = 1.8 V)", fontsize=13, fontweight="bold")
ax.set_xlim(0.25, 1.85)
ax.set_ylim(0, max(cs.max(), cl.max()) * 1.12)
ax.legend(loc="upper left", fontsize=10)
fig.tight_layout()
fig.savefig(os.path.join(HERE, "fcount_transfer_compare.png"), dpi=150)

print(f"schematic  : {ks:7.1f} counts/V   code@0.9V {np.interp(0.9,vs,cs):6.0f}   full-scale {cs.max():.0f}")
print(f"post-layout: {kl:7.1f} counts/V   code@0.9V {np.interp(0.9,vl,cl):6.0f}   full-scale {cl.max():.0f}")
print(f"sensitivity loss {100*(1-kl/ks):.1f} %   full-scale loss {100*(1-cl.max()/cs.max()):.1f} %")
