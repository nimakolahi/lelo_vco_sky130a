#!/usr/bin/env python3
"""Generate .sch + .sym library views for the 8 LELO_VCO device cells,
templated from the JNW_ATR pattern. The .mag layouts already exist."""
import os

DEST = "/Users/nima/EpsilonElectronic/Projects/VCO/aicex/ip/lelo_vco_sky130a/design/LELO_VCO_SKY130A"

# ---- schematic templates (placeholders __W__ __L__ __NF__) ----
NCH_SCH = """v {xschem version=3.0.0 file_version=1.2 }
G {}
K {}
V {}
S {}
E {}
C {devices/iopin.sym} 0 0 0 0 {name=p0 lab=D}
C {devices/iopin.sym} 0 20 0 0 {name=p1 lab=G}
C {devices/iopin.sym} 0 40 0 0 {name=p2 lab=S}
C {devices/iopin.sym} 0 60 0 0 {name=p3 lab=B}
C {sky130_fd_pr/nfet_01v8.sym} 400 0 0 0 {name=M1
L=__L__
W=__W__
nf=__NF__
mult=1
ad="'int((nf+1)/2) * W/nf * 0.29'"
pd="'2*int((nf+1)/2) * (W/nf + 0.29)'"
as="'int((nf+2)/2) * W/nf * 0.29'"
ps="'2*int((nf+2)/2) * (W/nf + 0.29)'"
nrd="'0.29 / W'" nrs="'0.29 / W'"
sa=0 sb=0 sd=0
model=nfet_01v8
spiceprefix=X
}
N 440.0 -30.0 420.0 -30.0 {lab=D}
C {devices/lab_pin.sym} 440.0 -30.0 2 0 {name=l0 sig_type=std_logic lab=D }
N 360.0 0.0 380.0 0.0 {lab=G}
C {devices/lab_pin.sym} 360.0 0.0 0 0 {name=l1 sig_type=std_logic lab=G }
N 440.0 30.0 420.0 30.0 {lab=S}
C {devices/lab_pin.sym} 440.0 30.0 2 0 {name=l2 sig_type=std_logic lab=S }
N 440.0 0.0 420.0 0.0 {lab=B}
C {devices/lab_pin.sym} 440.0 0.0 2 0 {name=l3 sig_type=std_logic lab=B }
"""

PCH_SCH = NCH_SCH.replace("nfet_01v8", "pfet_01v8")
# pfet: D and S wire positions swapped (matches ATR PCH template)
PCH_SCH = PCH_SCH.replace(
    "N 440.0 -30.0 420.0 -30.0 {lab=D}\nC {devices/lab_pin.sym} 440.0 -30.0 2 0 {name=l0 sig_type=std_logic lab=D }",
    "N 440.0 30.0 420.0 30.0 {lab=D}\nC {devices/lab_pin.sym} 440.0 30.0 2 0 {name=l0 sig_type=std_logic lab=D }")
PCH_SCH = PCH_SCH.replace(
    "N 440.0 30.0 420.0 30.0 {lab=S}\nC {devices/lab_pin.sym} 440.0 30.0 2 0 {name=l2 sig_type=std_logic lab=S }",
    "N 440.0 -30.0 420.0 -30.0 {lab=S}\nC {devices/lab_pin.sym} 440.0 -30.0 2 0 {name=l2 sig_type=std_logic lab=S }")

# ---- symbol views (generic, use @symname) ----
NCH_SYM = """v {xschem version=3.0.0 file_version=1.2 }
K {type=subcircuit
format="@name @pinlist @symname "
template="name=x1 "
}
L 4 30 10 40 15 {}
L 4 40 15 30 20 {}
L 4 20 -15 40 -15 {}
L 4 40 -15 40 -30 {}
L 4 20 15 40 15 {}
L 4 40 15 40 30 {}
L 4 20 0 40 0 {}
L 4 20 15 20 -15 {}
L 4 15 -15 15 15 {}
L 4 0 0 15 0 {}
T {@symname} 40 -20 0 0 0.16 0.16 { vcenter=true}
T {@name} 40 25 0 0 0.16 0.16 { vcenter=true}
B 5 36 -26 44 -34 {name=D dir=inout pinnumber=1}
B 5 -4 4 4 -4 {name=G dir=inout pinnumber=2}
B 5 36 34 44 26 {name=S dir=inout pinnumber=3}
B 5 36 4 44 -4 {name=B dir=inout pinnumber=4}
"""

PCH_SYM = """v {xschem version=3.0.0 file_version=1.2 }
K {type=subcircuit
format="@name @pinlist @symname "
template="name=x1 "
}
L 4 20 15 40 15 {}
L 4 40 15 40 30 {}
L 4 20 -15 40 -15 {}
L 4 40 -15 40 -30 {}
L 4 20 0 40 0 {}
L 4 37 -20 27 -15 {}
L 4 27 -15 37 -10 {}
L 4 20 15 20 -15 {}
L 4 15 -15 15 15 {}
A 4 11 0 4 0 360 {}
L 4 0 0 7 0 {}
T {@symname} 40 20 0 0 0.16 0.16 { vcenter=true}
T {@name} 40 -25 0 0 0.16 0.16 { vcenter=true}
B 5 36 34 44 26 {name=D dir=inout pinnumber=1}
B 5 -4 4 4 -4 {name=G dir=inout pinnumber=2}
B 5 36 -26 44 -34 {name=S dir=inout pinnumber=3}
B 5 36 4 44 -4 {name=B dir=inout pinnumber=4}
"""

# name, kind, W, L, nf
CELLS = [
    ("LELO_NCH_2p4x0p54",  "n", "2.4",  "0.54", "1"),
    ("LELO_NCH_0p96x0p36", "n", "0.96", "0.36", "1"),
    ("LELO_NCH_1p2x0p18",  "n", "1.2",  "0.18", "1"),
    ("LELO_NCH_96x0p9",    "n", "96",   "0.9",  "16"),
    ("LELO_PCH_4p8x0p54",  "p", "4.8",  "0.54", "1"),
    ("LELO_PCH_4p8x0p36",  "p", "4.8",  "0.36", "1"),
    ("LELO_PCH_2p4x0p36",  "p", "2.4",  "0.36", "1"),
    ("LELO_PCH_4p8x0p18",  "p", "4.8",  "0.18", "1"),
]

for name, kind, w, l, nf in CELLS:
    sch_tpl = NCH_SCH if kind == "n" else PCH_SCH
    sym_tpl = NCH_SYM if kind == "n" else PCH_SYM
    sch = sch_tpl.replace("__W__", w).replace("__L__", l).replace("__NF__", nf)
    with open(os.path.join(DEST, name + ".sch"), "w") as f:
        f.write(sch)
    with open(os.path.join(DEST, name + ".sym"), "w") as f:
        f.write(sym_tpl)
    print(f"  wrote {name}.sch + {name}.sym  (W={w} L={l} nf={nf})")

print("done")
