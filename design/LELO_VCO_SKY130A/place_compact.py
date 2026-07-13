#!/usr/bin/env python3
# Build a COMPACT Fig.8-column placement tcl (columns b..f = ring stages,
# a = bias, g = buffer, r = resistors). Reads real cell sizes from .mag.
import os, re

DES = "/Users/nima/EpsilonElectronic/Projects/VCO/aicex/ip/lelo_vco_sky130a/design/LELO_VCO_SKY130A"
TR  = "/Users/nima/EpsilonElectronic/Projects/VCO/aicex/ip/jnw_tr_sky130a/design/JNW_TR_SKY130A"

def bbox(cell):
    for d in (DES, TR):
        p = os.path.join(d, cell + ".mag")
        if os.path.exists(p):
            txt = open(p).read()
            m = re.search(r"string FIXED_BBOX\s+(-?\d+)\s+(-?\d+)\s+(-?\d+)\s+(-?\d+)", txt)
            if m:
                return tuple(int(v) for v in m.groups())
            # fallback: geometry bbox, skipping the checkpaint boundary layer
            xs, ys = [], []; layer = ""
            for ln in txt.splitlines():
                if ln.startswith("<<"):
                    layer = ln
                elif ln.startswith("rect") and "checkpaint" not in layer:
                    _, x1, y1, x2, y2 = ln.split()[:5]
                    xs += [int(x1), int(x2)]; ys += [int(y1), int(y2)]
            return (min(xs), min(ys), max(xs), max(ys))
    raise SystemExit("no cell " + cell)

def wh(cell):
    x1, y1, x2, y2 = bbox(cell); return x2 - x1, y2 - y1

# column -> list of (instname, cell) bottom..top
cols = {
 "a": [("a0","LELO_NCH_0p96x0p36"),("a1","LELO_NCH_96x0p9"),("a2","LELO_PCH_4p8x0p36"),("a3","LELO_PCH_2p4x0p36")],
 "b": [("b0","LELO_NCH_0p96x0p36"),("b1","LELO_NCH_2p4x0p54"),("b2","LELO_PCH_4p8x0p54"),("b3","LELO_PCH_4p8x0p36")],
 "c": [("c0","LELO_NCH_0p96x0p36"),("c1","LELO_NCH_2p4x0p54"),("c2","LELO_PCH_4p8x0p54"),("c3","LELO_PCH_4p8x0p36")],
 "d": [("d0","LELO_NCH_0p96x0p36"),("d1","LELO_NCH_2p4x0p54"),("d2","LELO_PCH_4p8x0p54"),("d3","LELO_PCH_4p8x0p36")],
 "e": [("e0","LELO_NCH_0p96x0p36"),("e1","LELO_NCH_2p4x0p54"),("e2","LELO_PCH_4p8x0p54"),("e3","LELO_PCH_4p8x0p36")],
 "f": [("f0","LELO_NCH_0p96x0p36"),("f1","LELO_NCH_2p4x0p54"),("f2","LELO_PCH_4p8x0p54"),("f3","LELO_PCH_4p8x0p36")],
 "g": [("g0","LELO_NCH_1p2x0p18"),("g1","LELO_NCH_1p2x0p18"),("g2","LELO_PCH_4p8x0p18"),("g3","LELO_PCH_4p8x0p18")],
 "r": [("x1","JNWTR_RES2"),("x2","JNWTR_RES4")],
}
order = ["a","b","c","d","e","f","g","r"]

GAP  = 320   # vertical gap between stacked cells (> nwell spacing ~256)
XGAP = 360   # horizontal gap between columns

lines = ["load LELO_VCO -force", "addpath ../JNW_TR_SKY130A",
         "select top cell", "if {[catch {delete}]} {}"]
x = 0
for cn in order:
    colw = max(wh(c)[0] for _, c in cols[cn])
    y = 0
    for inst, cell in cols[cn]:
        w, h = wh(cell)
        cx = x + colw // 2          # center the cell in the column
        cy = y + h // 2
        lines += [f"box {cx} {cy} {cx} {cy}", f"getcell {cell}", f"identify {inst}"]
        y += h + GAP
    x += colw + XGAP
lines += ["save", 'puts "PLACED_OK"', "quit -noprompt"]
open("/private/tmp/claude-501/-Users-nima-EpsilonElectronic-Projects-VCO/63c66204-c8d0-4157-82e4-195a536da1cd/scratchpad/compact.tcl","w").write("\n".join(lines)+"\n")
print("wrote compact.tcl; column widths:", {c: max(wh(x)[0] for _,x in cols[c]) for c in order})
