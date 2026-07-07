#!/usr/bin/env python3
"""Plot the mixed-signal frequency-counter demo (LELO_VCO + fcount).

Reads fcount_wave.dat written by ngspice `wrdata`:
    columns = time  dec_count  time  gate  time  Vout
dec_count is the counter value / 1000 (from the svinst bus decoder).
"""
import os
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

HERE = os.path.dirname(os.path.abspath(__file__))
DAT = os.path.join(HERE, "fcount_wave.dat")
PNG = os.path.join(HERE, "fcount_demo.png")
TGATE = 2e-6  # gate window [s] (matches tran.spi)

d = np.loadtxt(DAT)
t = d[:, 0] * 1e6            # us
count = d[:, 1] * 1000.0     # decode /1000 scaling -> integer count
gate = d[:, 3]
vout = d[:, 5]

final = int(round(count[gate > 0.9].max())) if np.any(gate > 0.9) else int(round(count.max()))
fmeas = final / TGATE / 1e6  # MHz implied by the count

# gate window extent (us)
gon = t[gate > 0.9]
g0, g1 = (gon.min(), gon.max()) if gon.size else (t.min(), t.max())

plt.style.use("seaborn-v0_8-whitegrid")
fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(8, 6), sharex=True,
                               gridspec_kw={"height_ratios": [1, 1.4]})

# top: analog VCO output
ax1.plot(t, vout, color="#2563eb", lw=0.5)
ax1.set_ylabel("V$_{out}$  [V]")
ax1.set_title("Mixed-signal frequency counter:  LELO_VCO  →  RTL fcount\n"
              "(typical, 27 °C, VDD = 1.8 V, V$_{in}$ = 0.9 V)",
              fontsize=12, fontweight="bold")
ax1.axvspan(g0, g1, color="#94a3b8", alpha=0.15)

# bottom: digital count staircase + gate window
ax2.axvspan(g0, g1, color="#94a3b8", alpha=0.15, label=f"gate window ({TGATE*1e6:.0f} µs)")
ax2.plot(t, count, color="#dc2626", lw=1.8, drawstyle="steps-post", label="counter value")
ax2.axhline(final, color="#dc2626", ls=":", lw=1)
ax2.annotate(f"result = {final} counts\n→ f$_{{out}}$ ≈ {fmeas:.1f} MHz",
             xy=(g1, final), xytext=(-10, -28), textcoords="offset points",
             ha="right", fontsize=10,
             bbox=dict(boxstyle="round", fc="white", ec="#dc2626"))
ax2.set_xlabel("time  [µs]")
ax2.set_ylabel("counter value")
ax2.legend(loc="upper left", fontsize=9, frameon=True)

fig.tight_layout()
fig.savefig(PNG, dpi=150)
print(f"Saved {PNG}")
print(f"result = {final} counts over {TGATE*1e6:.0f} us  ->  f_out ~= {fmeas:.2f} MHz")
