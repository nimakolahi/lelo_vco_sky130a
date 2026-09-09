#!/usr/bin/env python3
"""Schematic vs post-layout tuning curve for LELO_VCO.

Reads vco_tuning.dat (schematic, `make sweep`) and vco_tuning_lay.dat
(post-layout, `make sweep_lay`), overlays them, and reports Kvco over the
linear part of the sweep.  Points with fout <= 0 did not oscillate and are
dropped, as in plot_tuning.py.
"""
import os
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

HERE = os.path.dirname(os.path.abspath(__file__))

def load(fn):
    vin, fout = [], []
    with open(os.path.join(HERE, fn)) as f:
        for line in f:
            p = line.split()
            if len(p) < 2:
                continue
            try:
                v, fo = float(p[0]), float(p[1])
            except ValueError:
                continue
            if fo > 0:
                vin.append(v); fout.append(fo / 1e6)
    return np.array(vin), np.array(fout)

def kvco(v, f, lo=0.5, hi=1.3):
    m = (v >= lo) & (v <= hi)
    return np.polyfit(v[m], f[m], 1)[0]

vs, fs = load("vco_tuning.dat")
vl, fl = load("vco_tuning_lay.dat")

fig, ax = plt.subplots(figsize=(7, 4.5))
ax.plot(vs, fs, "o-", label=f"schematic  (Kvco {kvco(vs,fs):.1f} MHz/V)")
ax.plot(vl, fl, "s--", label=f"post-layout (Kvco {kvco(vl,fl):.1f} MHz/V)")
ax.set_xlabel("Vctrl [V]")
ax.set_ylabel("f_osc [MHz]")
ax.set_title("LELO_VCO tuning curve: schematic vs post-layout (tt, 27 C, 1.8 V)")
ax.grid(True, alpha=0.3)
ax.legend()
fig.tight_layout()
fig.savefig(os.path.join(HERE, "vco_tuning_lay.png"), dpi=140)

print(f"schematic : Kvco {kvco(vs,fs):6.1f} MHz/V   f(0.9V) {np.interp(0.9,vs,fs):6.2f} MHz   range {fs.min():.1f}-{fs.max():.1f} MHz")
print(f"post-layout: Kvco {kvco(vl,fl):6.1f} MHz/V   f(0.9V) {np.interp(0.9,vl,fl):6.2f} MHz   range {fl.min():.1f}-{fl.max():.1f} MHz")
slow = 100 * (1 - np.interp(0.9, vl, fl) / np.interp(0.9, vs, fs))
print(f"parasitic slowdown at 0.9 V: {slow:.1f} %")
