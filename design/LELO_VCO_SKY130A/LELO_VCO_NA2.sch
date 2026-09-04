v {xschem version=3.0.0 file_version=1.2 }
G {}
K {}
V {}
S {}
E {}
C {devices/iopin.sym} 0 0 0 0 {name=p0 lab=VSS}
C {devices/iopin.sym} 0 20 0 0 {name=p1 lab=net10}
C {devices/iopin.sym} 0 40 0 0 {name=p2 lab=net17}
C {devices/iopin.sym} 0 60 0 0 {name=p3 lab=net8}
C {LELO_VCO_SKY130A/LELO_NCH_0p96x0p36.sym} 400 0 0 0 {name=XXM12}
N 440.0 -50.0 440.0 -30.0 {lab=net11}
C {devices/lab_pin.sym} 440.0 -50.0 3 0 {name=l0 sig_type=std_logic lab=net11 }
N 380.0 0.0 400.0 0.0 {lab=net17}
C {devices/lab_pin.sym} 380.0 0.0 0 0 {name=l1 sig_type=std_logic lab=net17 }
N 440.0 50.0 440.0 30.0 {lab=VSS}
C {devices/lab_pin.sym} 440.0 50.0 1 0 {name=l2 sig_type=std_logic lab=VSS }
N 460.0 0.0 440.0 0.0 {lab=VSS}
C {devices/lab_pin.sym} 460.0 0.0 2 0 {name=l3 sig_type=std_logic lab=VSS }
C {LELO_VCO_SKY130A/LELO_NCH_2p4x0p54.sym} 400 170 0 0 {name=XXM2}
N 440.0 120.0 440.0 140.0 {lab=net10}
C {devices/lab_pin.sym} 440.0 120.0 3 0 {name=l4 sig_type=std_logic lab=net10 }
N 380.0 170.0 400.0 170.0 {lab=net8}
C {devices/lab_pin.sym} 380.0 170.0 0 0 {name=l5 sig_type=std_logic lab=net8 }
N 440.0 220.0 440.0 200.0 {lab=net11}
C {devices/lab_pin.sym} 440.0 220.0 1 0 {name=l6 sig_type=std_logic lab=net11 }
N 460.0 170.0 440.0 170.0 {lab=VSS}
C {devices/lab_pin.sym} 460.0 170.0 2 0 {name=l7 sig_type=std_logic lab=VSS }
