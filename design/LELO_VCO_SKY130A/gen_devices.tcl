# Generate the 8 LELO_VCO device cells into the design dir, DRC each.
proc gen {name kind w l nf} {
    load $name -force
    set p [sky130::sky130_fd_pr__${kind}_defaults]
    dict set p w $w
    dict set p l $l
    dict set p nf $nf
    sky130::sky130_fd_pr__${kind}_draw $p
    save ../design/LELO_VCO_SKY130A/$name.mag
    drc check
    drc catchup
    puts "DRCRESULT $name [drc count total]"
}

# NCH
gen LELO_NCH_2p4x0p54  nfet_01v8 2.4  0.54 1
gen LELO_NCH_0p96x0p36 nfet_01v8 0.96 0.36 1
gen LELO_NCH_1p2x0p18  nfet_01v8 1.2  0.18 1
gen LELO_NCH_96x0p9    nfet_01v8 96   0.9  16
# PCH
gen LELO_PCH_4p8x0p54  pfet_01v8 4.8  0.54 1
gen LELO_PCH_4p8x0p36  pfet_01v8 4.8  0.36 1
gen LELO_PCH_2p4x0p36  pfet_01v8 2.4  0.36 1
gen LELO_PCH_4p8x0p18  pfet_01v8 4.8  0.18 1

puts "ALLDONE"
quit -noprompt
