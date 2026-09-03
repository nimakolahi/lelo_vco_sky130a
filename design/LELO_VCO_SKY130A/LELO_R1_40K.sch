v {xschem version=3.0.0 file_version=1.2 }
G {}
K {}
V {}
S {}
E {}
C {devices/iopin.sym} 0 0 0 0 {name=p0 lab=R1}
C {devices/iopin.sym} 0 20 0 0 {name=p1 lab=R2}
C {devices/iopin.sym} 0 40 0 0 {name=p2 lab=B}
C {sky130_fd_pr/res_high_po.sym} 400 0 0 0 {name=XR0
W=0.35
L=43.83
model=res_high_po_0p35
mult=1}
N 420.0 -30.0 400.0 -30.0 {lab=R1}
C {devices/lab_pin.sym} 420.0 -30.0 2 0 {name=l0 sig_type=std_logic lab=R1 }
N 420.0 30.0 400.0 30.0 {lab=R2}
C {devices/lab_pin.sym} 420.0 30.0 2 0 {name=l1 sig_type=std_logic lab=R2 }
N 360.0 0.0 380.0 0.0 {lab=B}
C {devices/lab_pin.sym} 360.0 0.0 0 0 {name=l2 sig_type=std_logic lab=B }
