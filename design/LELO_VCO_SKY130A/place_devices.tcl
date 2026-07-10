# Hand-place LELO_VCO devices, well-spread so nothing overlaps (bypass cicpy).
load LELO_VCO -force
addpath ../JNW_TR_SKY130A
select top cell
if {[catch {delete}]} {}

# rows spaced 8000 apart (cells < ~1200 tall); x pitch 3000 (cells < ~600 wide)
set pmos {XM5 LELO_PCH_4p8x0p54 XM6 LELO_PCH_4p8x0p54 XM7 LELO_PCH_4p8x0p54 XM8 LELO_PCH_4p8x0p54 XM9 LELO_PCH_4p8x0p54 XM15 LELO_PCH_4p8x0p36 XM16 LELO_PCH_4p8x0p36 XM17 LELO_PCH_4p8x0p36 XM18 LELO_PCH_4p8x0p36 XM19 LELO_PCH_4p8x0p36 XM24 LELO_PCH_4p8x0p36 XM25 LELO_PCH_2p4x0p36 XM22 LELO_PCH_4p8x0p18 XM23 LELO_PCH_4p8x0p18}
set nmos {XM0 LELO_NCH_2p4x0p54 XM1 LELO_NCH_2p4x0p54 XM2 LELO_NCH_2p4x0p54 XM3 LELO_NCH_2p4x0p54 XM4 LELO_NCH_2p4x0p54 XM10 LELO_NCH_0p96x0p36 XM11 LELO_NCH_0p96x0p36 XM12 LELO_NCH_0p96x0p36 XM13 LELO_NCH_0p96x0p36 XM14 LELO_NCH_0p96x0p36 XM26 LELO_NCH_0p96x0p36 XM20 LELO_NCH_1p2x0p18 XM21 LELO_NCH_1p2x0p18}
set res  {x1 JNWTR_RES2 x2 JNWTR_RES4}

proc placerow {lst y} {
    set x 0
    foreach {inst cell} $lst {
        box $x $y $x $y
        getcell $cell
        identify $inst
        set x [expr {$x + 3000}]
    }
}
placerow $pmos 8000
placerow $nmos 0
placerow $res -8000
# the tall 96um device (XM27) alone, far left so its height overlaps nothing
box -12000 0 -12000 0
getcell LELO_NCH_96x0p9
identify XM27

save
puts "PLACED_OK"
quit -noprompt
