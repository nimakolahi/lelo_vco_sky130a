#!/usr/bin/env python3
# Post-process cicpy's LELO_VCO.mag: keep cicpy's column assignment and
# within-column ordering, but re-flow with real spacing so the guard-less
# gencell cells don't abut (which violated nwell/li/diff/metal spacing).
import re, sys

MAG = "/Users/nima/EpsilonElectronic/Projects/VCO/aicex/ip/lelo_vco_sky130a/design/LELO_VCO_SKY130A/LELO_VCO.mag"
VGAP = 320   # vertical gap between stacked cells (1.59um > nwell 1.27um)
HGAP = 400   # horizontal gap between columns

lines = open(MAG).read().splitlines()
head, insts, tail = [], [], []
i = 0
# header = everything up to first "use"
while i < len(lines) and not lines[i].startswith("use "):
    head.append(lines[i]); i += 1
while i < len(lines):
    if lines[i].startswith("use "):
        use = lines[i]
        tr  = lines[i+1]            # transform 1 0 c 0 1 f
        bx  = lines[i+2]            # box x1 y1 x2 y2
        nums = list(map(int, tr.split()[1:]))         # a b c d e f
        bxv  = list(map(int, bx.split()[1:]))         # x1 y1 x2 y2
        insts.append({"use": use, "tr": nums, "box": bxv})
        i += 3
    else:
        tail.append(lines[i]); i += 1

# cluster into columns by x1
cols = {}
for ins in insts:
    cols.setdefault(ins["box"][0], []).append(ins)
colx_sorted = sorted(cols)

new_colx = {}
cx = 0
for oldx in colx_sorted:
    new_colx[oldx] = cx
    maxw = max(c["box"][2] - c["box"][0] for c in cols[oldx])
    cx += maxw + HGAP

for oldx in colx_sorted:
    col = sorted(cols[oldx], key=lambda c: c["box"][1])   # bottom..top
    y = 0
    nx = new_colx[oldx]
    for c in col:
        x1, y1, x2, y2 = c["box"]
        w, h = x2 - x1, y2 - y1
        dx = nx - x1
        dy = y - y1
        c["tr"][2] += dx     # tx (c)
        c["tr"][5] += dy     # ty (f)
        c["box"] = [x1 + dx, y1 + dy, x2 + dx, y2 + dy]
        y += h + VGAP

out = list(head)
for ins in insts:
    out.append(ins["use"])
    out.append("transform " + " ".join(map(str, ins["tr"])))
    out.append("box " + " ".join(map(str, ins["box"])))
out += tail
open(MAG, "w").write("\n".join(out) + "\n")
print(f"re-spaced {len(insts)} instances across {len(cols)} columns (VGAP={VGAP}, HGAP={HGAP})")
print("new extents: x", min(new_colx.values()), "->", cx, " ; per-column base x:", {k: new_colx[k] for k in colx_sorted})
