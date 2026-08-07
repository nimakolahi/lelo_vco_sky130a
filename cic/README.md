# LELO_VCO — ciccreator (generated-layout) environment

Branch `ciccreator`. Goal: rebuild the VCO layout the way the reference LELO
blocks are built — describe it in a `.cic` and generate a clean, DRC/LVS-correct
layout (tapped cells, signals on M2) with ciccreator + cicpy, instead of hand-Magic.
(`master` keeps the hand layout for finishing by hand.)

## Why (see the reference family)
Every analogicus LELO oscillator is GENERATED, not hand-drawn:
  lelo_gr01/oscillator.cic, lelo_gr02/OSCILLATOR.cic, lelo_gr04/LELO_GR04_OSC_v2.cic
They instantiate the **jnw_atr** tapped cells (JNWATR_NCH/PCH_*) and route on M2.
The hand LELO_VCO used stripped cicpy gencells on M1 -> the fused mesh we fought.

## The flow (from tech/make/core.make `ip:` target)
    make ip     # 1) cic  ../cic/ip.json ../cic/sky130.tech LELO_VCO   -> LELO_VCO.cic
                # 2) cicpy transpile LELO_VCO.cic ../cic/sky130.tech LELO_VCO --magic ... -> .mag
    make view   # cicpy gui LELO_VCO.cic   (interactive place/route tweak)

## Tools
- ciccreator: cloned at `aicex/ciccreator` (C++/Qt). NEEDS BUILDING — no local qmake.
  Build inside the aicex docker image (has Qt), or just rely on the image's prebuilt `cic`:
      docker run --rm -v <aicex>:/home/aicex -w /home/aicex/ciccreator \
        wulffern/aicex:26.04_latest bash -lc 'qmake && make -j4'   # -> bin/cic
  (If `aicex/ciccreator/bin/cic` is absent, core.make falls back to `cic` on PATH = the image's build.)
- cicpy: in the aicex docker image (drives transpile + GUI).

## What's set up here (cic/)
- sky130.tech          — ciccreator tech (copied from jnw_atr)
- hand_placements.txt  — your 30 hand placements (rows) — the SEED for the .cic
- devices.txt          — the 8 device types (W/L) to map onto jnw_atr JNWATR_* cells

## Design steps (to do)
1. Build/verify `cic` and `cicpy` (docker, above).
2. Map each LELO device (devices.txt) to a JNWATR_* tapped-cell variant
   (by fingers/contacts) — see jnw_atr transistors.json / gr04 OSC .cic for examples.
3. Author `cic/ip.json` (top cell LELO_VCO): place the transistors in the 4 rows
   from hand_placements.txt, add JNWATR TAPTOP/TAPBOT tap cells per band.
4. Add the ROUTING on M2 per the LVS net checklist (net17->M26 diode, net18->M25 diode,
   ring hops, Vout, Vin) — same target list already verified against the schematic.
5. `make ip` -> `make drc lvs`. Iterate in `make view` (cicpy gui).

## Reference templates
- jnw_atr: cic/ip.py, ip.json, transistors.json (how tapped cells are declared)
- lelo_gr01 design/oscillator.cic (closest: ring oscillator) — study its M2 routing
