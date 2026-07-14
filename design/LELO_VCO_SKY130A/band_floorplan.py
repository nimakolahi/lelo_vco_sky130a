#!/usr/bin/env python3
# Paper-style BAND floorplan (Fig.8): rows bottom->top =
#   A: NMOS current sources + buffer NMOS + M26   (near GND)
#   B: ring NMOS (M0-M4)
#   C: ring PMOS (M5-M9)          <-- shared nwell
#   D: PMOS current sources + M24/M25 + buffer PMOS (near VDD)
# Left block: M27 (wide NMOS) + R1 (RES2/RES4).
# Then paint ONE nwell strip over rows C+D so all per-cell nwells merge.
import sys, os

DES="/Users/nima/EpsilonElectronic/Projects/VCO/aicex/ip/lelo_vco_sky130a/design/LELO_VCO_SKY130A"
TR ="/Users/nima/EpsilonElectronic/Projects/VCO/aicex/ip/jnw_tr_sky130a/design/JNW_TR_SKY130A"

# cell -> own bbox (llx,lly,urx,ury)
BB={
 "LELO_NCH_0p96x0p36":(-94,-184,94,184), "LELO_NCH_2p4x0p54":(-112,-328,112,328),
 "LELO_NCH_1p2x0p18":(-76,-208,76,208),  "LELO_NCH_96x0p9":(-1219,-1048,1219,1048),
 "LELO_PCH_4p8x0p54":(-148,-580,148,580),"LELO_PCH_4p8x0p36":(-130,-580,130,580),
 "LELO_PCH_2p4x0p36":(-130,-340,130,340),"LELO_PCH_4p8x0p18":(-112,-580,112,580),
 "JNWTR_RES2":(-18,-60,342,1380), "JNWTR_RES4":(-18,-60,558,1380),
}
def w(c): return BB[c][2]-BB[c][0]
def h(c): return BB[c][3]-BB[c][1]

# tunable gaps (magic units; ~202 units = 1um)
GAB=int(sys.argv[1]) if len(sys.argv)>1 else 180   # NMOS-NMOS row gap
GBC=int(sys.argv[2]) if len(sys.argv)>2 else 260   # N/P boundary (nwell edge)
GCD=int(sys.argv[3]) if len(sys.argv)>3 else 180   # PMOS-PMOS row gap
GX =int(sys.argv[4]) if len(sys.argv)>4 else 150   # column gap

# row baselines
hA,hB,hC,hD=416,656,1160,1160
yA=0
yB=yA+hA+GAB
yC=yB+hB+GBC
yD=yC+hC+GCD

# instance -> (slot, row, cell)
NC0="LELO_NCH_0p96x0p36"; NC1="LELO_NCH_2p4x0p54"; NCB="LELO_NCH_1p2x0p18"
PCC="LELO_PCH_4p8x0p54"; PCS="LELO_PCH_4p8x0p36"; P25="LELO_PCH_2p4x0p36"; PCB="LELO_PCH_4p8x0p18"
inst={
 # left block
 "a1":("M27","A","LELO_NCH_96x0p9"), "x1":("R1","A","JNWTR_RES2"), "x2":("R1","R2","JNWTR_RES4"),
 # row A (NMOS bottom)
 "a0":("bias1","A",NC0),
 "b0":("b","A",NC0),"c0":("c","A",NC0),"d0":("d","A",NC0),"e0":("e","A",NC0),"f0":("f","A",NC0),
 "g0":("buf1","A",NCB),"g1":("buf2","A",NCB),
 # row B (ring NMOS)
 "b1":("b","B",NC1),"c1":("c","B",NC1),"d1":("d","B",NC1),"e1":("e","B",NC1),"f1":("f","B",NC1),
 # row C (ring PMOS)
 "b2":("b","C",PCC),"c2":("c","C",PCC),"d2":("d","C",PCC),"e2":("e","C",PCC),"f2":("f","C",PCC),
 # row D (PMOS top)
 "a2":("bias1","D",PCS),"a3":("bias2","D",P25),
 "b3":("b","D",PCS),"c3":("c","D",PCS),"d3":("d","D",PCS),"e3":("e","D",PCS),"f3":("f","D",PCS),
 "g2":("buf1","D",PCB),"g3":("buf2","D",PCB),
}
row_y={"A":yA,"B":yB,"C":yC,"D":yD,"R2":yA+1440+80}  # R2 stacked above R1

# slot x (left->right), width = max cell width in slot
slots=["M27","R1","bias1","bias2","b","c","d","e","f","buf1","buf2"]
slotw={s:0 for s in slots}
for i,(s,r,c) in inst.items():
    slotw[s]=max(slotw[s],w(c))
slot_x={}; x=0
for s in slots:
    slot_x[s]=x; x+=slotw[s]+GX
    if s=="R1": x+=200   # extra clearance R1 -> PMOS band (nwell to res/ndiff)

lines=["load LELO_VCO -force","select top cell","if {[catch {delete}]} {}",
       "addpath ../JNW_TR_SKY130A"]
pmos=[]
for name,(s,r,c) in inst.items():
    llx=slot_x[s]; lly=row_y[r]
    # center cell in its slot horizontally
    llx += (slotw[s]-w(c))//2
    px=llx-BB[c][0]; py=lly-BB[c][1]     # getcell origin -> cell (0,0)
    lines+=[f"box {px} {py} {px} {py}",f"getcell {c}",f"identify {name}"]
    if c.startswith("LELO_PCH"):
        pmos.append((llx,lly,llx+w(c),lly+h(c)))
# shared nwell strip over all PMOS cells
nx1=min(p[0] for p in pmos); ny1=min(p[1] for p in pmos)
nx2=max(p[2] for p in pmos); ny2=max(p[3] for p in pmos)
lines+=[f"box {nx1} {ny1} {nx2} {ny2}","paint nwell","save",
        f'puts "NWELL {nx1} {ny1} {nx2} {ny2}"','puts "PLACED_OK"',"quit -noprompt"]
open("/private/tmp/claude-501/-Users-nima-EpsilonElectronic-Projects-VCO/63c66204-c8d0-4157-82e4-195a536da1cd/scratchpad/band.tcl","w").write("\n".join(lines)+"\n")
print(f"rows: A={yA} B={yB} C={yC} D={yD}; nwell x[{nx1},{nx2}] y[{ny1},{ny2}]; width~{x}")
