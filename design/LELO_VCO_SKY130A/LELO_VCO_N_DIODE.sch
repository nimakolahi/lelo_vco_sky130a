v {xschem version=3.0.0 file_version=1.2 }
G {}
K {}
V {}
S {}
E {}
C {devices/iopin.sym} 0 0 0 0 {name=p0 lab=VSS}
C {devices/iopin.sym} 0 20 0 0 {name=p1 lab=net17}
C {LELO_VCO_SKY130A/LELO_NCH_0p96x0p36.sym} 400 0 0 0 {name=XXM26}
N 440.0 -50.0 440.0 -30.0 {lab=net17}
C {devices/lab_pin.sym} 440.0 -50.0 3 0 {name=l0 sig_type=std_logic lab=net17 }
N 380.0 0.0 400.0 0.0 {lab=net17}
C {devices/lab_pin.sym} 380.0 0.0 0 0 {name=l1 sig_type=std_logic lab=net17 }
N 440.0 50.0 440.0 30.0 {lab=VSS}
C {devices/lab_pin.sym} 440.0 50.0 1 0 {name=l2 sig_type=std_logic lab=VSS }
N 460.0 0.0 440.0 0.0 {lab=VSS}
C {devices/lab_pin.sym} 460.0 0.0 2 0 {name=l3 sig_type=std_logic lab=VSS }
