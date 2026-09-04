v {xschem version=3.0.0 file_version=1.2 }
G {}
K {}
V {}
S {}
E {}
C {devices/iopin.sym} 0 0 0 0 {name=p0 lab=VSS}
C {devices/iopin.sym} 0 20 0 0 {name=p1 lab=net16}
C {LELO_VCO_SKY130A/LELO_R1_40K.sym} 400 0 0 0 {name=Xx1}
N 380.0 -20.0 380.0 0.0 {lab=net16}
C {devices/lab_pin.sym} 380.0 -20.0 3 0 {name=l0 sig_type=std_logic lab=net16 }
N 400.0 20.0 380.0 20.0 {lab=VSS}
C {devices/lab_pin.sym} 400.0 20.0 2 0 {name=l1 sig_type=std_logic lab=VSS }
N 380.0 60.0 380.0 40.0 {lab=VSS}
C {devices/lab_pin.sym} 380.0 60.0 1 0 {name=l2 sig_type=std_logic lab=VSS }
