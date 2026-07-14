#!/usr/bin/env python3
# Rewrite each device cell's << labels >> section: convert the rlabel D/S/G
# ports (on diff/poly) into flabel ports on the `locali` layer, which is the
# only thing cicpy's magic reader accepts (elif token=="flabel") and is
# electrically the same net (S/D via licon, gate via polycont).
import re, sys, os

DES = "/Users/nima/EpsilonElectronic/Projects/VCO/aicex/ip/lelo_vco_sky130a/design/LELO_VCO_SKY130A"
CELLS = ["LELO_NCH_0p96x0p36","LELO_NCH_2p4x0p54","LELO_NCH_1p2x0p18",
         "LELO_PCH_4p8x0p54","LELO_PCH_4p8x0p36","LELO_PCH_2p4x0p36","LELO_PCH_4p8x0p18"]

def localirects(txt):
    rects, inloc = [], False
    for ln in txt.splitlines():
        if ln.startswith("<< "):
            inloc = (ln.strip() == "<< locali >>")
        elif inloc and ln.startswith("rect"):
            _, x1, y1, x2, y2 = ln.split()[:5]
            rects.append((int(x1), int(y1), int(x2), int(y2)))
    return rects

def nearest(rects, px, py):
    def d(r):
        cx, cy = (r[0]+r[2])/2, (r[1]+r[3])/2
        return (cx-px)**2 + (cy-py)**2
    return min(rects, key=d)

for cell in CELLS:
    p = os.path.join(DES, cell + ".mag")
    txt = open(p).read()
    loc = localirects(txt)
    if not loc:
        print("!! no locali in", cell); continue
    # collect existing rlabel ports: name -> (px,py), skip duplicates keep first
    ports = []
    for m in re.finditer(r"^rlabel\s+\S+\s+(-?\d+)\s+(-?\d+)\s+(-?\d+)\s+(-?\d+)\s+\d+\s+(\S+)\s*$", txt, re.M):
        x1, y1, x2, y2, name = int(m[1]), int(m[2]), int(m[3]), int(m[4]), m[5]
        ports.append((name, (x1+x2)//2, (y1+y2)//2))
    # build flabels on nearest locali pad; ensure unique pad per port
    used = set(); flines = []
    for name, px, py in ports:
        cand = sorted(loc, key=lambda r: ((r[0]+r[2])/2-px)**2 + ((r[1]+r[3])/2-py)**2)
        r = next((c for c in cand if c not in used), cand[0]); used.add(r)
        flines.append(f"flabel locali s {r[0]} {r[1]} {r[2]} {r[3]} 0 FreeSans 400 0 0 0 {name}")
    # replace the labels section body
    newlabels = "<< labels >>\n" + "\n".join(flines) + "\n"
    txt2 = re.sub(r"<< labels >>\n.*?(?=<< )", newlabels, txt, count=1, flags=re.S)
    open(p, "w").write(txt2)
    print(f"{cell}: {[n for n,_,_ in ports]} -> flabel locali  ({len(loc)} locali pads)")
