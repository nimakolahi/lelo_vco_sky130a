# Regenerate LELO_VCO transistor leaf cells as sky130 PDK gencells WITH a
# substrate/well guard ring (guard 1) + D/G/S/B ports, at the EXACT schematic
# W/L. Run in Magic (sky130A) via: magic -dnull -rcfile <sky130A.magicrc> this.tcl
# Then post-process ports to flabel on metal1 (D/S/G) / locali (B) — see README.
# Sizes (type name W L nf) — M27 (96x0p9) is hand-drawn, NOT regenerated here.
proc gen {type name w l nf} {
    set p [sky130::sky130_fd_pr__${type}_defaults]
    dict set p w $w; dict set p l $l; dict set p nf $nf; dict set p guard 1
    sky130::sky130_fd_pr__${type}_draw $p
    save ./$name.mag
    flush [cellname list self]
}
gen nfet_01v8 LELO_NCH_0p96x0p36 0.96 0.36 1
gen nfet_01v8 LELO_NCH_1p2x0p18  1.2  0.18 1
gen nfet_01v8 LELO_NCH_2p4x0p54  2.4  0.54 1
gen pfet_01v8 LELO_PCH_2p4x0p36  2.4  0.36 1
gen pfet_01v8 LELO_PCH_4p8x0p18  4.8  0.18 1
gen pfet_01v8 LELO_PCH_4p8x0p36  4.8  0.36 1
gen pfet_01v8 LELO_PCH_4p8x0p54  4.8  0.54 1
quit -noprompt
