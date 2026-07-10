# Hand-place the LELO_VCO devices at sane grid coords (bypass cicpy).
load LELO_VCO -force
addpath ../JNW_TR_SKY130A
# clear any existing content
select top cell
if {[catch {delete}]} {}

# instance -> cell,  laid out in rows by type (user will re-arrange + route)
# PMOS row (top), NMOS row (bottom), resistors on the side. Spacing 4000 units.
set pmos {XM5 LELO_PCH_4p8x0p54 XM6 LELO_PCH_4p8x0p54 XM7 LELO_PCH_4p8x0p54 XM8 LELO_PCH_4p8x0p54 XM9 LELO_PCH_4p8x0p54 XM15 LELO_PCH_4p8x0p36 XM16 LELO_PCH_4p8x0p36 XM17 LELO_PCH_4p8x0p36 XM18 LELO_PCH_4p8x0p36 XM19 LELO_PCH_4p8x0p36 XM24 LELO_PCH_4p8x0p36 XM25 LELO_PCH_2p4x0p36 XM22 LELO_PCH_4p8x0p18 XM23 LELO_PCH_4p8x0p18}
set nmos {XM0 LELO_NCH_2p4x0p54 XM1 LELO_NCH_2p4x0p54 XM2 LELO_NCH_2p4x0p54 XM3 LELO_NCH_2p4x0p54 XM4 LELO_NCH_2p4x0p54 XM10 LELO_NCH_0p96x0p36 XM11 LELO_NCH_0p96x0p36 XM12 LELO_NCH_0p96x0p36 XM13 LELO_NCH_0p96x0p36 XM14 LELO_NCH_0p96x0p36 XM26 LELO_NCH_0p96x0p36 XM20 LELO_NCH_1p2x0p18 XM21 LELO_NCH_1p2x0p18 XM27 LELO_NCH_96x0p9}
set res  {x1 JNWTR_RES2 x2 JNWTR_RES4}

proc placerow {lst y} {
    set x 0
    foreach {inst cell} $lst {
        box $x $y $x $y
        getcell $cell
        identify $inst
        set x [expr {$x + 4000}]
    }
}
placerow $pmos 6000
placerow $nmos 0
placerow $res -6000

save
puts "PLACED_OK"
quit -noprompt
